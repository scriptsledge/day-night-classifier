[⬅️ Back to Main README](../README.md)

# 📚 Knowledge Base & Troubleshooting

## 1. Project Philosophy

### Why K-Nearest Neighbors (KNN)?
**Decision:** We selected KNN over Deep Learning (CNNs) for this specific problem.
**Rationale:**
*   **Interpretability:** KNN offers transparent logic ("This image looks like Night because its brightness is low, similar to other Night images"). Deep Learning models are often opaque "black boxes."
*   **Data Efficiency:** For small datasets (20 images), KNN performs robustly without the risk of overfitting that plagues complex neural networks.
*   **Educational Value:** It clearly demonstrates the impact of feature engineering (converting raw pixels to meaningful metrics like Contrast and Brightness).

### Q: Why is the 'Class' column empty?
**Design Choice:** The workflow enforces a **Human-in-the-Loop** process.
**Rationale:** Real-world Machine Learning is rarely fully automated. By requiring manual labeling, we demonstrate the critical role of the "Supervisor" in Supervised Learning. This demystifies the origin of ground truth data.

### Q: Why are the `.joblib` model files included in the repo?
**A:** To enable the **Instant Cloud Demo** on Streamlit Cloud.
*   **The Trade-off:** We committed the trained assets (`scaler.joblib`, `knn_model.joblib`) so the web app works immediately for visitors.
*   **The Workshop:** For the full educational experience, you should **delete these files** locally (`rm gui_app/assets/*.joblib`). This forces you to run the feature extraction and training scripts yourself.

---

## 2. Technical Troubleshooting Log

### Error: "Permission denied (os error 13)"
**Symptoms:** `uv run` fails to create the `.venv` directory.
**Root Cause:** Mixed usage of `sudo`/Docker and user-level commands. If Docker creates a file, it is owned by `root`. The standard user cannot modify it.
**Solution:** Recursively reclaim directory ownership.
```bash
sudo chown -R $USER:$USER .
```

### Error: "externally-managed-environment" (PEP 668)
**Symptoms:** `pip install` fails with a message about breaking system packages.
**Root Cause:** Modern Linux distributions protect system Python directories to prevent stability issues.
**Solution:** Do not use `pip` directly. Use **`uv`** (which creates isolated environments) or **Docker** (which encapsulates the environment).

### Error: "Package 'libgl1-mesa-glx' has no installation candidate"
**Symptoms:** Docker build fails during `apt-get install`.
**Root Cause:** The `python:3.9-slim` base image uses Debian repositories where this specific package name has been deprecated and replaced.
**Solution:** Update `Dockerfile` to install `libgl1` instead.

### Error: "KeyError: 'Class' not found in axis"
**Symptoms:** `train_and_save_model.py` crashes.
**Root Cause:** The `feature_table.csv` file was generated but not labeled. The script expects a 'Class' column to train the model.
**Solution:** Open the CSV file and manually fill in the 'Class' column (Day/Night) before training.

### Q: Why is `HostPath` volume used in `k8s/deployment.yaml`?
**A:** For this educational project running on a local Minikube cluster, `HostPath` allows the Kubernetes pod to directly access the files on your host machine. This is crucial for the "manual labeling" step where you edit `feature_table.csv` outside the container, and the changes are reflected inside. In a production cloud Kubernetes environment, you would typically use persistent storage solutions like `PersistentVolumeClaims` backed by cloud storage (e.g., EBS, Azure Disk, GCE Persistent Disk).

### Q: How do I add my own images?
**A:** The project is designed to scale! The filename convention (e.g., `01.jpg`, `21.jpg`) does not strictly matter. You can name your images descriptively (e.g., `my_vacation_day.jpg`, `dark_forest_night.png`).

1.  **Add Images:** Drop your `.jpg` or `.png` files into the `dataset/` folder. The script automatically detects these extensions. Files with other extensions (e.g., `.gif`, `.bmp`) will be ignored unless the script is modified.
2.  **Re-run Extractor:** Run `uv run feature_extractor.py`. This will regenerate `feature_table.csv` including your new images.
3.  **Label:** Open the CSV. Your new images will have empty 'Class' columns. Fill them with `Day` or `Night`. The `ImageName` column ensures you can match the row to the correct physical file.
4.  **Re-train:** Run `uv run train_and_save_model.py`. Your model is now smarter!

