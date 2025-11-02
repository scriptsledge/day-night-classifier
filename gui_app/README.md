# GUI for the Day/Night Scene Classifier

This application provides a simple web-based graphical user interface (GUI) to interact with the Day/Night scene classifier.

---

### How it Works

The application uses a K-Nearest Neighbors (KNN) model that was pre-trained on a set of 20 images with 4 objective features:

1.  **`brightness`**
2.  **`contrast`**
3.  **`colorfulness`**
4.  **`color_variety`**

The saved model (`knn_model.joblib`) and feature scaler (`scaler.joblib`) are located in the `assets/` directory.

When you upload an image, the application automatically calculates these four features, scales them, and feeds them to the trained model to get a prediction.

---

### How to Run the Application

1.  **Follow the installation instructions in the main [README.md](../README.md) file.**

2.  **Ensure the virtual environment is active.**

3.  **From the root directory of the project**, run the Streamlit app:
    ```bash
    streamlit run gui_app/app.py
    ```

4.  **View in your browser:**
    Streamlit will open a new tab in your web browser with the running application.