import easyocr
import numpy as np
from PIL import Image
import streamlit as st

st.header("🔍 EasyOCR Test")

uploaded = st.file_uploader("Upload an image to test OCR", type=["png", "jpg", "jpeg"])

if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="Uploaded Image")

    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(np.array(image))

    st.subheader("OCR Result")
    for _, text, _ in result:
        st.write(text)
