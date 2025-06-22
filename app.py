import streamlit as st
from utils import extract
from metadata_gen import generate_metadata
import json
import os
from datetime import datetime
from transformers import pipeline
from keybert import KeyBERT

# Streamlit UI setup
st.set_page_config(page_title="Auto Metadata Generator", layout="centered")
st.title("📄 Automated Metadata Generator")
st.markdown("Upload a document (`.pdf`, `.docx`, `.txt`) to get structured metadata.")

# File uploader
uploaded_file = st.file_uploader("Upload File", type=["pdf", "docx", "txt"])

@st.cache_resource
def get_summarizer():
    return pipeline("summarization", model="knkarthick/MEETING_SUMMARY")

@st.cache_resource
def get_kw_model():
    return KeyBERT(model="all-MiniLM-L6-v2")

if uploaded_file is not None:
    with st.spinner("🔍 Processing file and loading models..."):
        file_name = uploaded_file.name

        # Save file temporarily
        with open(file_name, "wb") as f:
            f.write(uploaded_file.read())

        try:
            # Extract full content and metadata
            extracted = extract(file_name)
            text = extracted["text"]
            author = extracted["author"]
            creation_date = extracted["creation_date"]

            # Load models
            summarizer = get_summarizer()
            kw_model = get_kw_model()

            # Generate metadata
            metadata = generate_metadata(
                text,
                summarizer,
                kw_model,
                author=author,
                subject=None,  # Removed subject input
                creation_date=creation_date or datetime.today().strftime("%Y-%m-%d")
            )

            # Add document name
            metadata["doc_name"] = file_name

            # Display metadata
            st.success("✅ Metadata Generated!")

            st.markdown("### 📄 Document Name")
            st.write(metadata['doc_name'])

            st.markdown("### 🏷️ Title")
            st.write(metadata['title'])

            st.markdown("### 👤 Author")
            st.write(metadata['author'])

            st.markdown("### 📅 Creation Date")
            st.write(metadata['creation_date'])

            st.markdown("### 🔑 Keywords")
            st.write(", ".join(metadata['keywords']))

            st.markdown("### 📚 Summary")
            st.write(metadata['summary'])

            # Download option
            st.download_button(
                label="📥 Download Metadata as JSON",
                data=json.dumps(metadata, indent=2),
                file_name="metadata.json",
                mime="application/json"
            )

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")

        finally:
            if os.path.exists(file_name):
                os.remove(file_name)
