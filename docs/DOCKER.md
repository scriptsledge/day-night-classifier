[⬅️ Back to Main README](../README.md)

# 🐳 Docker: Enterprise-Grade Reproducibility

## 1. Executive Summary
Docker is the industry standard for delivering software in isolated, reproducible packages called **containers**. By encapsulating the application with its specific operating system libraries and Python dependencies, Docker eliminates "it works on my machine" issues.

In this project, we leverage Docker to:
1.  **Isolate the Environment:** Bypass local system restrictions (like PEP 668).
2.  **Standardize Dependencies:** Ensure every user has the exact required libraries (e.g., `libgl1` for image processing).
3.  **Enable Hybrid Workflows:** We use **Volume Mounting** to allow you to edit files on your host machine while the code runs inside the container.

---

## 2. Prerequisites & Installation

To execute the containerized workflow, the Docker engine must be installed and active.

*   **Windows/macOS:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop).
*   **Linux:** Install [Docker Engine](https://docs.docker.com/engine/install/) for your distribution.

**Verification:**
Execute the following in your terminal to ensure the daemon is responsive:
```bash
docker run hello-world
```

---

## 3. The Deployment Lifecycle

We utilize a **stateful workflow** where data persists on your host machine despite the container being ephemeral.

### Phase 1: Build the Image
The `Dockerfile` defines the environment. Building the image compiles this definition into an executable artifact.

```bash
# Run from the project root directory
sudo docker build -t day-night-classifier .
```
*Note: This process installs system-level dependencies like `libgl1` which are critical for `opencv` and `pillow`.*

### Phase 2: The "Hands-On" Execution
We run the container in **interactive mode** with **volume mapping** and **port forwarding**.

**The Command:**
```bash
sudo docker run -p 8501:8501 -v $(pwd):/app -it day-night-classifier bash
```

**Breakdown of Flags:**
*   `-p 8501:8501`: **Critical.** Maps port 8501 inside the container (Streamlit) to port 8501 on your host (localhost). Without this, the web app is unreachable.
*   `-v $(pwd):/app`: **Volume Mount.** Maps your current directory (Host) to `/app` (Container). Changes made in one location are immediately reflected in the other.
*   `-it`: Allocates an interactive terminal session.

### Phase 3: Operational Workflow (Inside Container)

Once inside the container shell (`root@<id>:/app#`), execute the pipeline:

1.  **Feature Extraction:**
    ```bash
    python feature_extractor.py
    ```
    *Result:* `feature_table.csv` is created. Because of the volume mount, this file immediately appears on your host machine.

2.  **Manual Labeling (Host Action):**
    *   **Do not close the container.**
    *   Open `feature_table.csv` on your host machine using Excel or a text editor.
    *   Fill in the `Class` column (Day/Night).
    *   Save the file.

3.  **Model Training:**
    ```bash
    python train_and_save_model.py
    ```
    *Result:* The script reads your labeled CSV and saves the trained model (`.joblib` files) to `gui_app/assets/`.

4.  **Application Launch:**
    ```bash
    streamlit run gui_app/app.py
    ```
    *Access:* Open `http://localhost:8501` in your browser.

---

## 4. Troubleshooting & Edge Cases

### Issue: "Package 'libgl1-mesa-glx' has no installation candidate"
**Context:** During the build phase, older package names may become obsolete in newer base images (like Debian Trixie/Sid).
**Resolution:** We updated the `Dockerfile` to use the modern equivalent: `libgl1`.

### Issue: "Unable to connect" / Web App not loading
**Context:** The container is running, but the browser cannot reach it.
**Root Cause:** The container was started without port mapping. Docker isolates the container's network by default.
**Resolution:** You must restart the container including the `-p 8501:8501` flag.

### Concept: Persistence
**Observation:** If you restart the container, you **do not** need to re-label data or re-train the model.
**Reason:** Because of the volume mount (`-v`), the `feature_table.csv` and trained models in `gui_app/assets/` are stored on your **physical hard drive**, not inside the container. The container is simply a computation engine; the data lives with you.