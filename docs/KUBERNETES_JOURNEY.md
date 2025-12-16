[⬅️ Back to Main README](../README.md)

# 🛠️ Kubernetes Implementation Journey: Challenges & Solutions

This document serves as a technical log of the challenges encountered while containerizing and deploying the Day/Night Classifier to a local Kubernetes cluster (Minikube). It provides transparency into the "why" and "how" of our infrastructure decisions.

---

## 1. The Architecture: "Inception"
Running Kubernetes locally involves nested virtualization, which complicates file access and networking.

*   **Layer 1 (Host):** Your physical machine (`scriptSledge`). Holds the source code.
*   **Layer 2 (Minikube):** A Docker container acting as a Virtual Machine. It runs the Kubernetes control plane.
*   **Layer 3 (Pod):** The actual application container running *inside* Layer 2.

**The Challenge:** Layer 3 needs to read a file (`feature_table.csv`) from Layer 1. Layer 2 stands in the middle as a barrier.

---

## 2. Issue Log

### Issue 1: "Container creation is taking way more time"
**Symptoms:** `docker build` or `kubectl apply` hangs or takes 10+ minutes.
**Root Cause:**
1.  **Build Context Size:** Docker sends *all* files in the directory to the daemon before building. We had `env/` and `.venv/` folders (approx. 1.6GB) from previous local runs. Sending 1.6GB to the Minikube daemon is slow.
2.  **Resource Limits:** Minikube defaults to ~2 CPUs and 2GB RAM. Compiling libraries like `numpy` and `pandas` inside this constrained environment takes significantly longer than on the host.
**Solution:**
*   **Use `.dockerignore`:** Exclude `env/`, `.venv/`, `__pycache__/`, and `.git/` to reduce build context size (from GBs to MBs).
*   **Pre-pull Images:** Use `minikube cache add python:3.9-slim` to avoid re-downloading base images.

### Issue 2: "python: can't open file... No such file or directory"
**Symptoms:** The Pod starts, but crashes immediately with a "File not found" error when trying to run the app.
**Root Cause:**
We used a `hostPath` volume in `deployment.yaml` pointing to `/home/pyzard/coding/...`.
*   **Expectation:** Kubernetes looks at the *Host* filesystem.
*   **Reality:** When Minikube uses the Docker driver, `hostPath` refers to the filesystem *inside the Minikube container*, not your laptop. Minikube didn't have your code at that path.
**Solution:**
We switched strategies from direct mounting to **Copying**:
`minikube cp . /home/docker/day-night-classifier`
This physically copies files from Layer 1 (Host) to Layer 2 (Minikube), making them available for Layer 3 (Pod).

### Issue 3: "permission denied ... unix:///var/run/docker.sock"
**Symptoms:** `minikube start` or `minikube mount` fails.
**Root Cause:** The user (`pyzard`) was not in the `docker` group, or the session hadn't updated. Minikube requires access to the Docker daemon to spawn its cluster.
**Solution:**
1.  `sudo usermod -aG docker $USER`
2.  `newgrp docker` (or restart session).

### Issue 4: Persistence & Sync (The Mount Failure)
**Symptoms:** `minikube mount` runs without error, but the `/app` directory inside the Pod remains empty.
**Root Cause:** The complexity of the "Docker driver" for Minikube often leads to mounting inconsistencies, especially in nested environments. The mount might be mapping to the Minikube VM but not propagating correctly to the Pod's volume mount.
**Solution:**
We pivoted to a **Direct Transfer** strategy using `kubectl cp`.
1.  Start the Pod (initially empty).
2.  Push files directly: `kubectl cp . <pod-name>:/app`.
This bypasses the Minikube filesystem layer entirely and guarantees files arrive in the container.

### Issue 5: Networking Black Holes
**Symptoms:** `minikube service ... --url` returned an IP like `192.168.49.2`, but the browser said "Unable to connect" or "Timed out".
**Root Cause:** On Linux with the Docker driver, the Minikube network bridge is private. Your host machine (localhost) doesn't have a route to that `192.x` subnet. The `minikube tunnel` command attempts to fix this but requires sudo and can be flaky with permissions.
**Solution:**
**Port Forwarding.** Instead of trying to route *to* the cluster, we pipe the port *out*.
`kubectl port-forward svc/day-night-classifier-service 8501:8501`
This binds the Pod's port directly to `localhost:8501`, working 100% of the time regardless of driver or OS.

---

## 3. Performance Optimization Tips

If you rebuild frequently, speed up the process by creating a `.dockerignore` file in the project root:

```text
# .dockerignore
.git
.venv
env
__pycache__
dataset
gui_app/assets
```
This prevents heavy local folders from being sent to the Docker daemon, making builds almost instant.
