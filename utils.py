import os
from docx import Document
from PIL import Image
from io import BytesIO
import pdfplumber
import fitz
from zipfile import ZipFile
import easyocr
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)

def pdf_extract(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages).strip()

def ocr_pdf_extract(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_np = np.array(img) 
        result = reader.readtext(img_np)
        text += " ".join([txt for _, txt, _ in result]) + "\n"
    return text.strip()

def docx_extract(file_path):
    doc = Document(file_path)
    text = "\n".join(para.text for para in doc.paragraphs).strip()
    return text or ocr_docx_extract(file_path)

def ocr_docx_extract(file_path):
    text = ""
    with ZipFile(file_path) as docx_zip:
        for image_name in docx_zip.namelist():
            if image_name.startswith("word/media/"):
                with docx_zip.open(image_name) as img_file:
                    try:
                        image = Image.open(BytesIO(img_file.read()))
                        img_np = np.array(image)
                        result = reader.readtext(img_np)
                        text += " ".join([txt for _, txt, _ in result]) + "\n"
                    except:
                        pass
    return text.strip()

def txt_extract(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def extract(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = pdf_extract(file_path)
        return text or ocr_pdf_extract(file_path)
    elif ext == ".docx":
        return docx_extract(file_path)
    elif ext == ".txt":
        return txt_extract(file_path)
    else:
        raise ValueError("Unsupported file format.")
