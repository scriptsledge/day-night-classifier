[⬅️ Back to Project Root](../README.md)

# 📚 Project Documentation Hub

Welcome to the technical documentation for the Day/Night Classifier. Here you will find in-depth guides on the infrastructure and tooling decisions made for this project.

## 🚀 Deployment Guides

*   **[🐳 Docker Guide](./DOCKER.md)**  
    Learn how to build, run, and troubleshoot the Docker container. Explains the "Persistence" strategy using volume mounts.

*   **[☸️ Kubernetes Guide](./KUBERNETES.md)**  
    The definitive "User Manual" for deploying this app to a local Minikube cluster. Uses a robust `kubectl cp` + `port-forward` strategy.

*   **[⚡ uv Guide](./UV_GUIDE.md)**  
    Why we ditched `pip` for `uv`. Explains how `uv` handles PEP 668 restrictions and speeds up development.

## 🛠️ Engineering Logs

*   **[⚠️ Post-Mortem & Troubleshooting](./PROJECT_POSTMORTEM.md)**  
    A transparent log of every error encountered (Permissions, Networking, Deprecated Packages) and the exact fix. **Start here if something breaks.**

*   **[🪜 Kubernetes Journey](./KUBERNETES_JOURNEY.md)**  
    A "Developer Diary" chronicling the architectural challenges of running K8s inside Docker (Nested Virtualization) and why standard mounting failed.

*   **[❓ Knowledge Base (FAQ)](./FAQ.md)**  
    Answers to common questions: "Why is the CSV empty?", "Why KNN?", and general troubleshooting.
