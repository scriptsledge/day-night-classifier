import streamlit as st
from PIL import Image
import numpy as np
import joblib
from skimage.color import rgb2hsv
import os
import pandas as pd

# --- Page Config ---
st.set_page_config(
    page_title="Day/Night Classifier",
    page_icon="🌗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Styling ---
st.markdown("""
<style>
    .metric-card {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #464b5c;
        text-align: center;
    }
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Feature Calculation Function ---
def calculate_features(image):
    """
    Calculates the 4 features for a single image.
    """
    try:
        img_array = np.array(image.convert('RGB'))

        # 1. Grayscale features
        gray_img = image.convert('L')
        gray_array = np.array(gray_img)
        brightness = gray_array.mean()
        contrast = gray_array.std()

        # 2. HSV features
        hsv_array = rgb2hsv(img_array)
        colorfulness = hsv_array[:, :, 1].mean()
        color_variety = hsv_array[:, :, 0].std()

        return np.array([[brightness, contrast, colorfulness, color_variety]])
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

# --- Load Model and Scaler ---
@st.cache_resource
def load_assets():
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    try:
        scaler = joblib.load(os.path.join(assets_dir, 'scaler.joblib'))
        model = joblib.load(os.path.join(assets_dir, 'knn_model.joblib'))
        le_classes = joblib.load(os.path.join(assets_dir, 'label_encoder.joblib'))
        return scaler, model, le_classes
    except FileNotFoundError:
        return None, None, None

scaler, model, label_encoder_classes = load_assets()

# --- Sidebar ---
with st.sidebar:
    st.title("🌗 Control Panel")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    
    st.info("""
    **Model Architecture:**
    - **Type:** K-Nearest Neighbors (KNN)
    - **K:** 3 Neighbors
    - **Distance:** Euclidean
    """)
    
    st.divider()
    st.caption("v2.0.0 | MLOps Edition")

# --- Main Interface ---
st.title("Day/Night Analysis Dashboard")

if uploaded_file is None:
    st.warning("⚠️ Waiting for input data. Please upload an image in the sidebar.")
    st.stop()

if model is None:
    st.error("🚨 **System Error:** Model assets not found.")
    st.markdown("Please run `uv run train_and_save_model.py` locally to generate the required artifacts.")
    st.stop()

# --- Processing ---
image = Image.open(uploaded_file)
features = calculate_features(image)

if features is not None:
    # Scale features
    scaled_features = scaler.transform(features)
    
    # Predict
    prediction_idx = model.predict(scaled_features)[0]
    prediction_label = label_encoder_classes[prediction_idx]
    probs = model.predict_proba(scaled_features)[0]
    confidence = np.max(probs)

    # --- Layout ---
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("1. Visual Input")
        st.image(image, use_column_width=True, caption=f"Source: {uploaded_file.name}")

    with col2:
        st.subheader("2. Feature Extraction Engine")
        
        # Display Metrics in a Grid
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Brightness", f"{features[0][0]:.2f}", help="Mean pixel intensity (Grayscale)")
        m2.metric("Contrast", f"{features[0][1]:.2f}", help="Standard deviation of pixel intensity")
        m3.metric("Colorfulness", f"{features[0][2]:.2f}", help="Mean Saturation (HSV)")
        m4.metric("Color Var.", f"{features[0][3]:.2f}", help="Std Dev of Hue (HSV)")

        st.divider()

        st.subheader("3. Model Inference")
        
        # Result Banner
        if prediction_label == 'Day':
            st.success(f"### Prediction: **DAY** ☀️")
        else:
            st.info(f"### Prediction: **NIGHT** 🌙")
            
        st.progress(float(confidence), text=f"Confidence Level: {confidence*100:.1f}%")

        # --- Deep Dive / Debugging ---
        with st.expander("🔍 Deep Tech Analysis (Vector Space)", expanded=True):
            tab1, tab2 = st.tabs(["Feature Vectors", "Nearest Neighbors"])
            
            with tab1:
                st.code(f"Raw Input Vector:\n{features}", language="json")
                st.code(f"Scaled Vector (Z-Score):\n{scaled_features}", language="json")
                
            with tab2:
                # Find nearest neighbors
                distances, indices = model.kneighbors(scaled_features)
                st.write(f"The model looked at the **3 closest images** in the dataset:")
                
                neighbor_df = pd.DataFrame({
                    "Neighbor ID": indices[0],
                    "Distance (Euclidean)": distances[0]
                })
                st.dataframe(neighbor_df, hide_index=True)
                st.caption("*Lower distance = Higher similarity*")
