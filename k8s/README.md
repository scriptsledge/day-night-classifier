[⬅️ Back to Project Root](../README.md)

# ☸️ Kubernetes Manifests

This directory contains the configuration files required to deploy the Day/Night Classifier to a Kubernetes cluster.

## Files
*   **`deployment.yaml`**: Defines the application Pod, including the Docker image to use (`day-night-classifier:latest`) and the volume configuration for persistence.
*   **`service.yaml`**: Defines the networking Service to expose the Pod's port (8501) to the outside world (or Minikube bridge).

## Usage
These files are used in the "Enterprise Way" workflow.

```bash
kubectl apply -f k8s/
```

For full deployment instructions, including Minikube setup and troubleshooting, please read the **[Kubernetes Guide](../docs/KUBERNETES.md)**.
