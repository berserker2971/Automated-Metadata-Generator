import streamlit as st
from utils import extract
from metadata_gen import generate_metadata
import json

st.set_page_config(page_title="Auto Metadata Generator", layout="centered")

st.title("📄 Automated Metadata Generator")
st.markdown("Upload a document (`.pdf`, `.docx`, `.txt`) and get structured metadata.")

uploaded_file = st.file_uploader("Upload File", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    with st.spinner("🔍 Processing file..."):
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        try:
            text = extract(uploaded_file.name)
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