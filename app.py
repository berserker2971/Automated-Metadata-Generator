import streamlit as st
from utils import extract
from metadata_gen import generate_metadata
import json
import os

st.set_page_config(page_title="Auto Metadata Generator", layout="centered")

st.title("📄 Automated Metadata Generator")
st.markdown("Upload a document (`.pdf`, `.docx`, `.txt`) — **Max size: 5MB**")

uploaded_file = st.file_uploader(
    "Upload File",
    type=["pdf", "docx", "txt"]
)
if uploaded_file is not None:
    if uploaded_file.size > 5_000_000:
        st.error("❌ File too large. Please upload a file smaller than 5MB.")
        st.stop()
    with st.spinner("🔍 Processing file..."):
        file_path = uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        try:
            text = extract(file_path)
            metadata = generate_metadata(text)

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
