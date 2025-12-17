[⬅️ Back to Main README](../README.md)

# ☁️ Cloud Deployment Guide

This project is deployed live at: **[https://daynightclassifier.streamlit.app/](https://daynightclassifier.streamlit.app/)**

## 1. Streamlit Community Cloud (Recommended)

We use Streamlit Community Cloud for hosting because it offers a seamless integration with GitHub and requires zero infrastructure management.

### Prerequisites
*   A GitHub account.
*   The project pushed to a public repository.
*   **Crucial:** The trained model files (`gui_app/assets/*.joblib`) must be present in the repository.

### Deployment Steps
1.  **Sign Up/Login:** Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub account.
2.  **New App:** Click "New app".
3.  **Configuration:**
    *   **Repository:** `your-username/day-night-classifier`
    *   **Branch:** `main`
    *   **Main file path:** `gui_app/app.py`
4.  **Deploy:** Click the "Deploy!" button.

### The "Pre-trained" Trade-off
To make the Cloud Demo work instantly ("Zero Click"), we committed the trained model files (`.joblib`) to the repository. 

*   **Pros:** Instant gratification. The link works immediately.
*   **Cons:** It bypasses the "Hands-On" training step.
*   **Resolution:** For the educational workshop, we instruct users to **delete** these files locally to force a re-training cycle.

---

## 2. Docker / PaaS Deployment (Alternative)

Since the project includes a `Dockerfile`, it can be deployed to any container platform (Render, Railway, Fly.io, AWS App Runner).

### Steps
1.  Connect your GitHub repo to the provider.
2.  Point the provider to the `Dockerfile` in the root.
3.  **Port:** Ensure the provider listens on port `8501`.
4.  **Build Command:** The default `docker build` works.
5.  **Start Command:** `streamlit run gui_app/app.py`

*Note: Free tiers on these platforms may spin down (sleep) after inactivity, causing a delay on the first request.*
