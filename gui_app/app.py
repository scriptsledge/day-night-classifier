import streamlit as st
from PIL import Image
import numpy as np
import joblib
from skimage.color import rgb2hsv
import os

# --- Feature Calculation Function ---
# This function is self-contained to keep the GUI app portable.
def calculate_features(image_path):
    """
    Calculates the 4 features for a single image.
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)

        gray_img = img.convert('L')
        gray_array = np.array(gray_img)
        brightness = gray_array.mean()
        contrast = gray_array.std()

        hsv_array = rgb2hsv(img_array)
        colorfulness = hsv_array[:, :, 1].mean()
        color_variety = hsv_array[:, :, 0].std()

        return np.array([[brightness, contrast, colorfulness, color_variety]])
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

# --- Load Model and Scaler ---
# Construct an absolute path to the assets directory
assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
scaler = joblib.load(os.path.join(assets_dir, 'scaler.joblib'))
model = joblib.load(os.path.join(assets_dir, 'knn_model.joblib'))
label_encoder_classes = joblib.load(os.path.join(assets_dir, 'label_encoder.joblib'))

# --- Streamlit App UI ---
st.title("Day or Night? Image Classifier")
st.write("Upload an image and the model will predict whether it's a day or night scene.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # --- Prediction Logic ---
    st.write("")
    st.write("Classifying...")

    # Calculate features for the uploaded image
    features = calculate_features(uploaded_file)

    if features is not None:
        # Scale the features
        scaled_features = scaler.transform(features)

        # Make a prediction
        prediction_index = model.predict(scaled_features)[0]
        prediction = label_encoder_classes[prediction_index]

        # Display the result
        if prediction == 'Day':
            st.success(f"Prediction: **{prediction}** ☀️")
        else:
            st.info(f"Prediction: **{prediction}** 🌙")
