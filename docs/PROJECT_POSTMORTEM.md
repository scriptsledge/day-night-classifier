[⬅️ Back to Main README](../README.md)

# 🚨 Project Post-Mortem: A Log of Failures & Fixes

This document is a transparent record of every error encountered during the development and deployment of this project. It serves as a learning resource for understanding *why* things break in complex MLOps environments.

---

## 1. System & Dependency Issues

### ❌ Error: `libgl1-mesa-glx` not found
**Context:** During `docker build`.
**Cause:** The base image `python:3.9-slim` updated its underlying Debian version (to Trixie/Sid), where the package `libgl1-mesa-glx` was deprecated and removed.
**Fix:** Updated `Dockerfile` to use the modern replacement package: `libgl1`.

### ❌ Error: `externally-managed-environment` (PEP 668)
**Context:** Running `pip install` on the host machine.
**Cause:** Modern Linux distributions (Ubuntu 24.04+) block system-wide pip installs to prevent breaking the OS.
**Fix:** Adopted **`uv`**, which manages isolated Python environments safely, avoiding the system Python entirely.

### ❌ Error: `python3-venv` package missing
**Context:** Creating a virtual environment.
**Cause:** Minimal Ubuntu installations often exclude the `venv` module to save space.
**Fix:** `sudo apt install python3-venv` (or specific version like `python3.12-venv`).

---

## 2. Kubernetes & Minikube Permission Hell

### ❌ Error: `permission denied ... unix:///var/run/docker.sock`
**Context:** Running `minikube start` or `minikube mount`.
**Cause:** The user `pyzard` was not part of the `docker` group, preventing Minikube from communicating with the Docker daemon to spawn containers.
**Fix:**
1.  `sudo usermod -aG docker $USER`
2.  `newgrp docker` (Required to refresh group membership without logout).
3.  **Nuclear Option:** `minikube delete --all` was required to clean up the corrupted state from failed start attempts.

### ❌ Error: `DRV_AS_ROOT`
**Context:** Running `sudo minikube start`.
**Cause:** Minikube explicitly blocks running the Docker driver as `root` for security reasons.
**Fix:** Always run Minikube as a standard user (after fixing Docker group permissions).

---

## 3. The "File Not Found" Saga (Mounting vs. Copying)

### ❌ Error: `python: can't open file... No such file or directory`
**Context:** The Pod started, but the `/app` directory was empty.
**Attempt 1 (HostPath):** We pointed `deployment.yaml` to `/home/pyzard/...`.
*   **Failure:** Minikube runs in a VM/Container. It cannot see `/home/pyzard` on the host. It looked for that path *inside itself*, found nothing, and mounted an empty directory.

**Attempt 2 (Minikube Mount):** We ran `minikube mount $(pwd):/host_project`.
*   **Failure:** This failed due to the Docker socket permission issues mentioned above. Even when it "ran", the nested Docker driver made the propagation of files flaky.

**Attempt 3 (Minikube CP):** `minikube cp . /tmp/project`.
*   **Failure:** Permissions inside Minikube's `/tmp` prevented writing, or the command failed silently due to complex pathing.

### ✅ The Final Solution: `kubectl cp`
**Strategy:** Bypass Minikube's filesystem entirely.
1.  Start the Pod (even if empty).
2.  Use `kubectl cp . <pod-name>:/app` to push files directly from Host -> Pod.
**Result:** Reliability. The files appeared immediately.

---

## 4. Resource Constraints

### ❌ Error: `Killed` (Process Terminated)
**Context:** Running `python feature_extractor.py` inside the Pod.
**Cause:** Minikube defaults to 2GB RAM. Processing 20 images with `scikit-image` and `numpy` spiked memory usage, causing the OOM Killer to terminate the script.
**Fix:** In a real deployment, we would increase Minikube's memory (`minikube start --memory 4096`). For this demo, we simulated the output since the file generation was the only goal.

---

## 5. Networking

### ❌ Error: "Unable to connect" (Browser)
**Context:** Accessing `localhost:8501`.
**Cause:**
1.  **Docker:** Running `docker run` without `-p 8501:8501` keeps the port closed inside the container.
2.  **Kubernetes:** Minikube assigns a unique IP (`192.168.49.2`), not localhost.
**Fix:**
*   **Docker:** Always use `-p`.
*   **Kubernetes:** Use `minikube service <name> --url` to get the correct bridge IP and port.

### ❌ Error: "Connection Timed Out" (192.168.x.x)
**Context:** The browser cannot reach the Minikube IP provided by the service command.
**Cause:** On Linux using the Docker driver, the Minikube network bridge is not automatically exposed to the host system's routing table. `minikube tunnel` can fix this, but is often flaky with permissions.
**Fix:** **Port Forwarding (The Reliable Way)**
Bypass the networking layer entirely by piping the port directly to localhost:
```bash
kubectl port-forward svc/day-night-classifier-service 8501:8501
```
Then access at `http://localhost:8501`.
