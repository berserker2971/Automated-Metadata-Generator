from transformers import pipeline
from keybert import KeyBERT
import streamlit as st

@st.cache_resource
def get_summarizer():
    return pipeline("summarization", model="philschmid/bart-large-cnn-samsum")

@st.cache_resource
def get_kw_model():
    return KeyBERT(model="all-MiniLM-L6-v2")

summarizer = get_summarizer()
kw_model = get_kw_model()

def extract_title(text, title_len=20):
    for line in text.strip().split('\n'):
        if line.strip() and len(line.strip().split()) <= title_len:
            return line.strip()
    return "No Title"

def generate_summary(text, max_len=350):
    words = text.split()
    if len(words) < 40:
        return text.strip()
    
    summaries = []
    chunk_size = 400  # keep this below token limits
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        try:
            summary = summarizer(chunk, max_length=max_len, min_length=30, do_sample=False)[0]['summary_text']
            summaries.append(summary)
        except Exception as e:
            st.warning(f"Summarization failed on chunk: {e}")
            continue

        if len(summaries) >= 2:
            break

    return " ".join(summaries).strip()

def extract_keywords(text, top_n=5):
    try:
        keywords = kw_model.extract_keywords(text, top_n=top_n, stop_words='english')
        return [kw for kw, _ in keywords]
    except Exception as e:
        st.warning(f"Keyword extraction failed: {e}")
        return []

def generate_metadata(text):
    return {
        "title": extract_title(text),
        "summary": generate_summary(text),
        "keywords": extract_keywords(text)
    }
