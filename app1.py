import easyocr
import numpy as np
from PIL import Image
import streamlit as st
import fitz  # PyMuPDF
import gc

st.set_page_config(page_title="EasyOCR PDF Test", layout="centered")
st.header("📄 EasyOCR on PDF")

uploaded = st.file_uploader("Upload a PDF to test OCR", type=["pdf"])

if uploaded:
    # Save uploaded PDF temporarily
    pdf_path = "temp_uploaded.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded.read())

    # Initialize EasyOCR once
    st.info("Initializing EasyOCR Reader...")
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)

    st.info("Processing PDF...")
    extracted_text = ""

    try:
        doc = fitz.open(pdf_path)
        for page_num, page in enumerate(doc):
            st.write(f"### Page {page_num + 1}")
            try:
                # Lower DPI to reduce memory usage
                pix = page.get_pixmap(dpi=150)  # was 300
                mode = "RGB" if pix.alpha == 0 else "RGBA"
                img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
                img = img.convert("L")  # Grayscale for OCR
                st.image(img, caption=f"Page {page_num + 1}", use_column_width=True)

                img_np = np.array(img)
                result = reader.readtext(img_np)
                page_text = "\n".join([text for _, text, _ in result])
                extracted_text += page_text + "\n"

                st.code(page_text)

                # Clear memory per page
                del img, img_np, result, page_text, pix
                gc.collect()

            except Exception as e:
                st.error(f"Failed on page {page_num + 1}: {e}")

        st.subheader("📜 Full Extracted Text")
        st.text_area("Text", extracted_text, height=300)

    except Exception as e:
        st.error(f"Failed to open PDF: {e}")
