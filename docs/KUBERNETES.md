[⬅️ Back to Main README](../README.md)

# ☸️ Kubernetes (K8s): The Enterprise Workflow

## 1. Introduction
Kubernetes (K8s) is the industry standard for container orchestration. While Docker runs a container, Kubernetes manages it—handling networking, storage, and scaling.

This guide provides a **robust, battle-tested workflow** to deploy the Day/Night Classifier on a local Kubernetes cluster using Minikube. We use a specific strategy (`kubectl cp` + `port-forward`) to ensure reliability across all operating systems.

---

## 2. Prerequisites

1.  **Minikube:** [Install Guide](https://minikube.sigs.k8s.io/docs/start/)
2.  **Kubectl:** [Install Guide](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
3.  **Docker:** [Install Guide](https://docs.docker.com/get-docker/)

**Sanity Check:**
Run `minikube version` and `kubectl version --client` to ensure tools are ready.

---

## 3. Deployment Steps

### Step 1: Start the Cluster
Start Minikube with the Docker driver.
```bash
# If you encounter permission errors, run: 
# sudo usermod -aG docker $USER && newgrp docker
minikube start --driver=docker
```

### Step 2: Build the Image
We must build the Docker image *inside* Minikube so the cluster can see it.
```bash
eval $(minikube docker-env)
docker build -t day-night-classifier:latest .
```

### Step 3: Deploy the Pod
We use a persistent Pod that stays alive, allowing us to interact with it.
```bash
kubectl apply -f k8s/
```
*Wait for the pod to start:*
```bash
kubectl wait --for=condition=ready pod -l app=day-night-classifier --timeout=60s
```

### Step 4: Transfer Code (`kubectl cp`)
Because local volume mounting can be flaky on some systems (especially Linux with the Docker driver), we use direct copying to guaranteed file availability.
```bash
# Get the pod name dynamically
POD=$(kubectl get pods -o jsonpath="{.items[0].metadata.name}")

# Copy current directory into the Pod's /app folder
kubectl cp . $POD:/app
```

### Step 5: Run the ML Pipeline (Inside the Pod)
Now we execute the "Hands-On" steps inside the running cluster.
```bash
# Enter the pod
kubectl exec -it $POD -- bash
```

**Inside the Pod terminal:**
```bash
# 1. Generate Data
python feature_extractor.py

# 2. Label Data (Mocking the user action for speed)
# You can edit feature_table.csv manually if you have an editor installed,
# or paste the cheat sheet content.
echo "ImageName,brightness,contrast,colorfulness,color_variety,Class" > feature_table.csv
echo "01.jpg,139.6355,42.8660,0.1780,0.2950,Day" >> feature_table.csv
# ... (See README for full CSV content) ...

# 3. Train
python train_and_save_model.py

# 4. Launch App (Background)
nohup streamlit run gui_app/app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
```
*Type `exit` to return to your host terminal.*

### Step 6: Access the App
We bypass complex networking (NodePorts/LoadBalancers) by forwarding the port directly to your machine.
```bash
kubectl port-forward svc/day-night-classifier-service 8501:8501
```
**Open your browser to:** [http://localhost:8501](http://localhost:8501)

---

## 4. Why this approach?
You might wonder why we didn't use `minikube mount`.
*   **Reliability:** Mounting host filesystems into Minikube (which is itself a container) is prone to permission errors and sync issues on Linux.
*   **Production Parity:** `kubectl cp` and `port-forward` are standard tools used when interacting with remote production clusters, making this a valuable skill.

For a detailed log of the technical challenges that led to this workflow, read the **[Kubernetes Journey & Debugging Log](./KUBERNETES_JOURNEY.md)**.
