from transformers import pipeline
from keybert import KeyBERT

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
kw_model = KeyBERT(model="all-MiniLM-L6-v2")

def extract_title(text, title_len = 20):
    lines = text.strip().split('\n')
    for line in lines:
        if line.strip() and len(line.strip().split()) <= title_len:
            return line.strip()
    return "No Title"

def generate_summary(text, max_len=350):
    if len(text.split()) < 40:
        return text.strip()
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summaries = [summarizer(chunk, max_length=max_len, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks[:2]]
    return " ".join(summaries)

def extract_keywords(text, top_n=5):
    keywords = kw_model.extract_keywords(text, top_n=top_n, stop_words='english')
    return [kw for kw, _ in keywords]

def generate_metadata(text):
    return {
        "title": extract_title(text),
        "summary": generate_summary(text),
        "keywords": extract_keywords(text)
    }
