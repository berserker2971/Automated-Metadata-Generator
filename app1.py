import easyocr
import numpy as np
from PIL import Image
import streamlit as st
import fitz  # PyMuPDF

st.set_page_config(page_title="EasyOCR PDF Test", layout="centered")
st.header("📄 EasyOCR on PDF")

uploaded = st.file_uploader("Upload a PDF to test OCR", type=["pdf"])

if uploaded:
    # Save uploaded PDF temporarily
    pdf_path = "temp_uploaded.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded.read())

    # Load PDF
    st.info("Processing PDF...")
    doc = fitz.open(pdf_path)
    reader = easyocr.Reader(['en'], gpu=False)
    extracted_text = ""

    for page_num, page in enumerate(doc):
        st.write(f"### Page {page_num + 1}")
        try:
            # Convert page to image
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            st.image(img, caption=f"Page {page_num + 1}", use_column_width=True)

            # OCR
            img_np = np.array(img)
            result = reader.readtext(img_np)

            page_text = "\n".join([text for _, text, _ in result])
            extracted_text += page_text + "\n"

            st.code(page_text)
        except Exception as e:
            st.error(f"Failed on page {page_num + 1}: {e}")

    # Show all text
    st.subheader("📜 Full Extracted Text")
    st.text_area("Text", extracted_text, height=300)
