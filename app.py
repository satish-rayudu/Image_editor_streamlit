import streamlit as st
import cv2
from filters import *
from utils import *

# Page Config
st.set_page_config(
    page_title="Pro Image Editor",
    page_icon="📸",
    layout="wide"
)

# Professional Dark Theme
st.markdown("""
<style>

.main {
    background-color: #0d1117;
    color: white;
}

h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}

section[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #30363d;
}

.stButton>button {
    background-color: #238636;
    color: white;
    border-radius: 8px;
    border: none;
    height: 3em;
    font-weight: 600;
    transition: 0.2s;
}

.stButton>button:hover {
    background-color: #2ea043;
}

.stDownloadButton>button {
    background-color: #1f6feb;
    color: white;
    border-radius: 8px;
    border: none;
    height: 3em;
    font-weight: 600;
}

.stDownloadButton>button:hover {
    background-color: #388bfd;
}

[data-testid="stFileUploader"] {
    background-color: #161b22;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #30363d;
}

.stSlider label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<h1 style='text-align:center;
font-size:50px;
color:#58a6ff;'>
📸 Image Editor
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center;
font-size:18px;
color:#8b949e;'>
Professional Image Processing Tool
</p>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("""
<h2 style='color:#f472b6;'>🎚️ Editor Console</h2>
""", unsafe_allow_html=True)

blur = st.sidebar.slider("🌫 Blur", 1, 51, 1)
sharpness = st.sidebar.slider("📏 Sharpness", 0.0, 3.0, 0.0)
brightness = st.sidebar.slider("🔆 Brightness", -100, 100, 0)
contrast = st.sidebar.slider("🌓 Contrast", 0.5, 3.0, 1.0)

gray = st.sidebar.checkbox("⚫ Grayscale")
edge = st.sidebar.checkbox("🖊 Edge Detection")

t1 = st.sidebar.slider("🔹 Threshold 1", 0, 255, 100)
t2 = st.sidebar.slider("🔸 Threshold 2", 0, 255, 200)

if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()

# Upload
st.markdown("## 📂 Upload Your Image")

uploaded_file = st.file_uploader(
    "Drop your image here",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file is None:
    st.info("👆 Upload an image to start editing")




# Processing
if uploaded_file is not None:

    image = load_image(uploaded_file)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    processed = image.copy()

    if blur > 1:
        processed = apply_blur(processed, blur)

    if sharpness > 0:
        processed = apply_sharpness(processed, sharpness)

    if brightness != 0:
        processed = adjust_brightness(processed, brightness)

    if contrast != 1.0:
        processed = adjust_contrast(processed, contrast)

    if gray:
        processed = to_grayscale(processed)

    if edge:
        processed = edge_detection(processed, t1, t2)

    # Preview
    st.markdown("## Preview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Original")
        st.image(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
            use_container_width=True
        )

    with col2:
        st.markdown("### Edited")
        st.image(
            cv2.cvtColor(processed, cv2.COLOR_BGR2RGB),
            use_container_width=True
        )

    # Download
    st.markdown("## Export Image")

    img_bytes = convert_to_bytes(processed)

    st.download_button(
        label="Download Image",
        data=img_bytes,
        file_name="edited_image.png",
        mime="image/png"
    )