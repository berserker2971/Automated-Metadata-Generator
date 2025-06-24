
# 📄 Auto Metadata Generator

An AI-powered Streamlit web application designed to **automatically extract and generate rich, structured metadata** from document formats like `.pdf`, `.docx`, and `.txt`. Leveraging natural language processing and modern file analysis tools, it transforms raw files into machine-readable summaries enriched with **titles, keywords, authorship, creation date**, and more. This application is particularly useful for tasks involving **semantic document indexing**, **digital archiving**, **automated tagging**, and **content classification**.

Whether you're managing thousands of documents in a digital library or want to extract quick insights from a research paper or meeting notes — this app significantly cuts down manual work and improves document discoverability.

👉 **Live App**: [automated-metadata-generator.streamlit.app](https://automated-metadata-generator.streamlit.app/)  
🎥 **Demo Video**: [Watch the Demo](https://youtu.be/qkDKGK_8cCY)

---

## 💡 What It Does

This app automates metadata extraction by analyzing the document text and metadata to generate:

- 🏷️ A representative **title**
- 📚 A concise **summary**
- 🔑 The most relevant **keywords**
- 📄 **File name** and **type**
- 👤 **Author** 
- 📅 **Creation date** 

---

## 🔧 How It Works

When you upload a document:

1. **Text is extracted** using:
   - `pdfplumber` for PDFs
   - `python-docx` for Word files
   - direct reading for `.txt` files

2. If the document has **no extractable text** (e.g. scanned PDFs or images), the app automatically uses **OCR with EasyOCR**.

3. It then runs NLP tasks:
   - 🧠 **Summarization** using `knkarthick/MEETING_SUMMARY`
   - 🔑 **Keyword extraction** using KeyBERT
   - 🏷️ **Title extraction** from the first meaningful short line in the document

4. It also pulls embedded metadata like:
   - 👤 **Author name**
   - 📅 **Creation date**

5. You can view and **download the complete metadata as JSON**.

---

## 🖥️ Running the App Locally

> ⚠️ **Use Python 3.10**  
> Do **not** use Python 3.13 — some dependencies like `transformers` may not yet fully support it.

### 1. Clone the Repository

```bash
git clone https://github.com/berserker2971/Automated-Metadata-Generator
cd Automated-Metadata-Generator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the App

```bash
python -m streamlit run app.py
```

Go to [http://localhost:8501](http://localhost:8501) to use the app.

---

## 📁 Project Structure

```
├── app.py              # Streamlit UI
├── utils.py            # File I/O, OCR, and extraction
├── metadata_gen.py     # NLP-based metadata generation
├── sample_files        # Example input documents
├── demo.mp4            # Demo video walkthrough
├── requirements.txt    # List of dependencies
└── README.md           # This documentation
```

---

## 🗂️ Supported Formats

- `.pdf` — if no text is found, OCR kicks in
- `.docx` — if no text is found, OCR kicks in
- `.txt` — direct read

---

## 📤 Metadata Output

| Field             | Description                                                   |
|------------------|---------------------------------------------------------------|
| 📄 `doc_name`     | Name of the uploaded file                                     |
| 📁 `file_type`    | File extension (e.g., `pdf`, `docx`, `txt`)                   |
| 🏷️ `title`        | First meaningful short line extracted from content            |
| 👤 `author`       | Extracted from file metadata (if available)                   |
| 📅 `creation_date`| Extracted from file metadata (if available)                   |
| 🔑 `keywords`     | Top keywords from content using KeyBERT                       |
| 📚 `summary`      | Compressed, readable version of the full document             |

---

## 📥 Download as JSON

Once processed, you can click a button to **download all the metadata** as a structured `.json` file, which is perfect for:

- Knowledge base ingestion
- Content indexing
- AI pipelines
- Internal search engines
- Digital archiving systems

---

## 🚀 Features – In Depth

### 📄 1. Document Upload (PDF, DOCX, TXT)
Supports the most common formats used in research, documentation, and content workflows.

### 🧾 2. File Parsing & OCR Fallback
If there's no text (like in scanned images), OCR with EasyOCR recovers content automatically.

### 🧠 3. Summarization
Uses a transformer model to condense long documents into short, high-level summaries.

### 🔑 4. Keyword Extraction
Extracts top semantic keywords using KeyBERT — useful for tagging, filtering, and categorization.

### 🏷️ 5. Title Generation
Heuristically chooses a strong title from early content in the document.

### 👤 6. Author Extraction
If author metadata is embedded in the file (like Word doc properties or PDF tags), it is auto-extracted.

### 📅 7. Creation Date
The app extracts the original creation date from the file’s metadata (when available).

### 📥 8. Download as JSON
Ready-to-use metadata file for integration into any backend or information system.

---

## 🧠 Tech Stack

| Component        | Library / Model                                                |
|------------------|----------------------------------------------------------------|
| UI               | Streamlit                                                      |
| Summarization    | `knkarthick/MEETING_SUMMARY` (Hugging Face)                    |
| Keywords         | KeyBERT                                                        |
| PDF Parsing      | pdfplumber                                                     |
| DOCX Reading     | python-docx                                                    |
| OCR              | EasyOCR                                                        |

---

## 📬 Feedback & Contributions

- Open issues or pull requests on the [GitHub repo](https://github.com/berserker2971/Automated-Metadata-Generator)
- Feature suggestions welcome!
- If you find this tool helpful, a ⭐️ is appreciated!
