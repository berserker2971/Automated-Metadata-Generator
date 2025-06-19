FROM python:3.10

# Install system dependencies for OCR
RUN apt update && apt install -y \
    poppler-utils \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0

WORKDIR /app
COPY . /app

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.enableCORS=false"]
