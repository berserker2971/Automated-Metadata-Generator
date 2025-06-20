import os
import gc
import re
import numpy as np
from docx import Document
from PIL import Image
from io import BytesIO
from zipfile import ZipFile
import pdfplumber
import fitz
import streamlit as st
import easyocr

@st.cache_resource
def get_ocr_reader():
    return easyocr.Reader(['en'], gpu=False)

def pdf_extract(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages).strip()

def ocr_pdf_extract(file_path, max_pages=3):
    text = ""
    reader = get_ocr_reader()
    
    try:
        with fitz.open(file_path) as doc:
            for i, page in enumerate(doc):
                if i >= max_pages:
                    break
                try:
                    pix = page.get_pixmap(dpi=300)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    img_np = np.array(img)

                    result = reader.readtext(img_np)
                    text += " ".join([txt for _, txt, _ in result]) + "\n"

                    # Cleanup
                    del pix, img, img_np, result
                    gc.collect()

                except Exception as e:
                    st.warning(f"OCR failed on page {i+1}: {e}")
    finally:
        del reader
        gc.collect()

    return text.strip()

def docx_extract(file_path):
    doc = Document(file_path)
    text = "\n".join(para.text for para in doc.paragraphs).strip()
    return text or ocr_docx_extract(file_path)

def ocr_docx_extract(file_path):
    text = ""
    reader = get_ocr_reader()

    try:
        with ZipFile(file_path) as docx_zip:
            for image_name in docx_zip.namelist():
                if image_name.startswith("word/media/"):
                    with docx_zip.open(image_name) as img_file:
                        try:
                            image = Image.open(BytesIO(img_file.read()))
                            img_np = np.array(image)

                            result = reader.readtext(img_np)
                            text += " ".join([txt for _, txt, _ in result]) + "\n"

                            del image, img_np, result
                            gc.collect()
                        except Exception as e:
                            st.warning(f"OCR failed on image {image_name}: {e}")
    finally:
        del reader
        gc.collect()

    return text.strip()

def txt_extract(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def clean_text(text):
    text = re.sub(r"\n+", "\n", text)                     # Collapse multiple newlines
    text = re.sub(r"\s{2,}", " ", text)                   # Collapse excess spaces
    text = re.sub(r"[^\w\s.,;:?!'\-]", '', text)          # Remove weird symbols
    return text.strip()

def extract(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = pdf_extract(file_path)
        if not text:
            st.info("No text detected in PDF, attempting OCR...")
            text = ocr_pdf_extract(file_path)
    elif ext == ".docx":
        text = docx_extract(file_path)
    elif ext == ".txt":
        text = txt_extract(file_path)
    else:
        raise ValueError("Unsupported file format.")

    return clean_text(text)
