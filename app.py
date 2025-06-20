import streamlit as st
from utils import extract
from metadata_gen import generate_metadata
import json
import os
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
        # Save file
        file_path = uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        try:
            text = extract(file_path)

            # Load models only after file is ready
            summarizer = get_summarizer()
            kw_model = get_kw_model()

            metadata = generate_metadata(text, summarizer, kw_model)

            st.success("✅ Metadata Generated!")
            st.markdown("### 🏷️ Title")
            st.write(metadata['title'])

            st.markdown("### 📚 Summary")
            st.write(metadata['summary'])

            st.markdown("### 🔑 Keywords")
            st.write(", ".join(metadata['keywords']))

            st.download_button(
                label="📥 Download Metadata as JSON",
                data=json.dumps(metadata, indent=2),
                file_name="metadata.json",
                mime="application/json"
            )

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
