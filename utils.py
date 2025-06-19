import numpy as np
import os
from fpdf import FPDF
import pdfplumber
from pdf2image import convert_from_path
import easyocr
import tempfile
import pypandoc

reader = easyocr.Reader(['en'])

def txt_to_pdf(txt_path, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            pdf.multi_cell(0, 10, line)
    pdf.output(pdf_path)

def convert_docx_to_pdf_pandoc(docx_path, pdf_path):
    try:
        pypandoc.convert_file(docx_path, 'pdf', outputfile=pdf_path)
    except Exception as e:
        raise RuntimeError(f"Pandoc failed to convert {docx_path}") from e

def pdf_extract(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

def ocr_pdf_extract(file_path):
    text = ""
    with tempfile.TemporaryDirectory() as temp_dir:
        images = convert_from_path(file_path, dpi=300, output_folder=temp_dir)
        for img in images:
            result = reader.readtext(np.array(img))
            text += ' '.join([res[1] for res in result]) + "\n"
    return text.strip()

def convert_pdf(file_path):
    base, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        return file_path
    elif ext == ".docx":
        pdf_path = base + ".converted.pdf"
        convert_docx_to_pdf_pandoc(file_path, pdf_path)
        return pdf_path
    elif ext == ".txt":
        pdf_path = base + ".converted.pdf"
        txt_to_pdf(file_path, pdf_path)
        return pdf_path
    else:
        raise ValueError("Unsupported file format.")

def extract(file_path):
    path = convert_pdf(file_path)
    text = pdf_extract(path)
    if not text.strip():
        text = ocr_pdf_extract(path)

    if path != file_path and path.endswith(".converted.pdf") and os.path.exists(path):
        os.remove(path)

    return text
