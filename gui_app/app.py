import streamlit as st
from PIL import Image
import numpy as np
import joblib
from skimage.color import rgb2hsv
import os
import pandas as pd

# --- 1. CONFIGURATION & ASSETS ---
icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')

st.set_page_config(
    page_title="Day/Night Vision",
    page_icon=icon_path,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CATPPUCCIN MOCHA PALETTE ---
# The definitive colors for the theme
mocha = {
    "base": "#1e1e2e",       # Main Background
    "mantle": "#181825",     # Sidebar Background
    "surface0": "#313244",   # Card/Input Background
    "surface1": "#45475a",   # Lighter Card
    "overlay0": "#6c7086",   # Borders
    "text": "#cdd6f4",       # Main Text
    "subtext0": "#a6adc8",   # Secondary Text
    "peach": "#fab387",      # Day Accent
    "blue": "#89b4fa",       # Night Accent
    "green": "#a6e3a1",      # Success/Online
    "red": "#f38ba8"         # Error/Offline
}

# --- 3. PROFESSIONAL MOCHA CSS ---
st.markdown(f"""
<style>
    /* 1. Global Reset */
    .stApp {{
        background-color: {mocha['base']};
        color: {mocha['text']};
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {mocha['mantle']};
        border-right: 1px solid {mocha['overlay0']};
    }}
    
    /* 2. Typography */
    h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, p, li {{
        color: {mocha['text']} !important;
        font-family: 'Inter', sans-serif;
    }}
    .stCaption {{
        color: {mocha['subtext0']} !important;
    }}

    /* 3. Result Cards (The "Mocha" Way: Dark bg + Colored Border) */
    .result-card {{
        background-color: {mocha['surface0']};
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }}
    
    /* 4. Inputs & File Uploader */
    /* The dropzone box */
    [data-testid="stFileUploaderDropzone"] {{
        background-color: {mocha['surface0']};
        border: 1px dashed {mocha['overlay0']};
        border-radius: 8px;
    }}
    /* The "Drag and drop..." text */
    [data-testid="stFileUploaderDropzone"] div div::before {{
        color: {mocha['subtext0']};
    }}
    [data-testid="stFileUploaderDropzone"] button {{
        background-color: {mocha['surface1']};
        color: {mocha['text']};
        border: 1px solid {mocha['overlay0']};
    }}
    
    /* 5. DataFrame Styling */
    [data-testid="stDataFrame"] {{
        background-color: {mocha['surface0']};
        border: 1px solid {mocha['overlay0']};
        border-radius: 8px;
    }}
    
    /* 6. Expanders */
    .streamlit-expanderHeader {{
        background-color: {mocha['surface0']};
        color: {mocha['text']};
        border-radius: 8px;
    }}
    
    /* 7. Image Captions */
    [data-testid="stImageCaption"] {{
        color: {mocha['subtext0']};
        background-color: {mocha['mantle']}; /* Subtle pill background for caption */
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-top: 5px;
    }}

    /* 8. Top Header (Deploy button, hamburger menu) */
    [data-testid="stHeader"] {{
        background-color: {mocha['base']} !important; /* Match app background */
        color: {mocha['text']} !important;
    }}
    
    [data-testid="stHeader"] svg {{ /* Icons */
        fill: {mocha['text']} !important;
    }}
    
    [data-testid="stToolbar"] {{ /* Toolbar container */
        background-color: {mocha['base']} !important;
    }}

</style>
""", unsafe_allow_html=True)

# --- 4. HELPER FUNCTIONS ---
def calculate_features(image):
    """Calculates the 4 features for a single image."""
    try:
        img_array = np.array(image.convert('RGB'))

        # Grayscale features
        gray_img = image.convert('L')
        gray_array = np.array(gray_img)
        brightness = gray_array.mean()
        contrast = gray_array.std()

        # HSV features
        hsv_array = rgb2hsv(img_array)
        colorfulness = hsv_array[:, :, 1].mean()
        color_variety = hsv_array[:, :, 0].std()

        return np.array([[brightness, contrast, colorfulness, color_variety]])
    except Exception as e:
        st.error(f"Processing Error: {e}")
        return None

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

# --- 5. SIDEBAR ---
with st.sidebar:
    st.image(icon_path, width=80)
    st.markdown("### Control Hub")
    
    uploaded_file = st.file_uploader("Input Source", type=["jpg", "jpeg", "png"], help="Upload an image to analyze")
    
    st.divider()
    
    with st.expander("⚙️ System Config", expanded=False):
        st.markdown(f"""
        <div style='color: {mocha['subtext0']}'>
        <b>Model Specs:</b><br>
        - Algorithm: KNN (k=3)<br>
        - Metric: Euclidean<br>
        - Latency: <100ms
        </div>
        """, unsafe_allow_html=True)
        
    st.caption("v2.2.0 | Enterprise Edition")

# --- 6. MAIN INTERFACE ---

# Header Section
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("Day/Night Vision System")
    st.markdown(f"<span style='color:{mocha['subtext0']}'>AI-powered environmental illumination analysis.</span>", unsafe_allow_html=True)
with col_head2:
    if model:
        st.markdown(f"<div style='text-align:right; color:{mocha['green']}; padding-top:20px;'>● <b>System Online</b></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:right; color:{mocha['red']}; padding-top:20px;'>● <b>System Offline</b></div>", unsafe_allow_html=True)

if not model:
    st.warning("Model artifacts missing. Please run the training script.")
    st.stop()

if uploaded_file is None:
    st.info("👋 **Ready for Analysis.** Please upload an image via the sidebar to begin.")
    st.stop()

# --- PROCESSING ---
image = Image.open(uploaded_file)
features = calculate_features(image)

if features is not None:
    # Inference
    scaled_features = scaler.transform(features)
    prediction_idx = model.predict(scaled_features)[0]
    prediction_label = label_encoder_classes[prediction_idx]
    probs = model.predict_proba(scaled_features)[0]
    confidence = np.max(probs)

    # --- NEW SPLIT LAYOUT ---
    st.divider()
    
    # Define Main Columns: Left (Image) and Right (Results & Data)
    col_left, col_right = st.columns([1.5, 1], gap="large")

    # --- LEFT COLUMN: Visual Input ---
    with col_left:
        st.subheader("Visual Input")
        # Display image with full container width
        st.image(image, use_container_width=True, caption=f"Source: {uploaded_file.name}")

    # --- RIGHT COLUMN: Analysis ---
    with col_right:
        # 1. Result Card (Top of Right Column)
        st.subheader("Classification")
        
        # Using styled container instead of block color for better integration
        if prediction_label == 'Day':
            st.markdown(
                f"""
                <div class='result-card' style='border: 2px solid {mocha['peach']};'>
                    <h2 style='color: {mocha['peach']}; margin:0; font-size: 2rem;'>☀️ DAYTIME</h2>
                    <p style='margin:0; margin-top:5px; color: {mocha['text']};'>Confidence: <b>{confidence*100:.1f}%</b></p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class='result-card' style='border: 2px solid {mocha['blue']};'>
                    <h2 style='color: {mocha['blue']}; margin:0; font-size: 2rem;'>🌙 NIGHTTIME</h2>
                    <p style='margin:0; margin-top:5px; color: {mocha['text']};'>Confidence: <b>{confidence*100:.1f}%</b></p>
                </div>
                """, 
                unsafe_allow_html=True
            )

        # 2. Feature Data Table (Below Result)
        st.subheader("Telemetry")
        
        feature_data = {
            "Metric": ["Brightness", "Contrast", "Colorfulness", "Color Var."],
            "Raw": [features[0][0], features[0][1], features[0][2], features[0][3]],
            "Norm. (Z)": [scaled_features[0][0], scaled_features[0][1], scaled_features[0][2], scaled_features[0][3]]
        }
        df_display = pd.DataFrame(feature_data)

        st.dataframe(
            df_display,
            column_config={
                "Metric": st.column_config.TextColumn("Metric", width="small"),
                "Raw": st.column_config.NumberColumn("Raw", format="%.1f"),
                "Norm. (Z)": st.column_config.ProgressColumn(
                    "Normalized",
                    format="%.2f",
                    min_value=-3,
                    max_value=3,
                ),
            },
            hide_index=True,
            use_container_width=True
        )

        # 3. Technical Details (Collapsible)
        st.markdown("---")
        with st.expander("🔍 Deep Diagnostics"):
            st.caption("**Vector Space Analysis**")
            st.code(f"Vec: {scaled_features[0].round(2)}", language="python")
            
            distances, indices = model.kneighbors(scaled_features)
            st.caption("**Nearest Neighbors (Training Set)**")
            neighbor_df = pd.DataFrame({
                "ID": indices[0],
                "Dist": distances[0]
            })
            st.dataframe(neighbor_df, hide_index=True, use_container_width=True)
