import streamlit as st
from datetime import datetime

def extract_title(text, title_len=25):
    lines = text.strip().split('\n')
    line=lines[0]
    for i in lines:
        if(len(i)>=5):
            line = i
            break  
    title=""
    for word in line.strip().split():
        if word[0].isupper() and len(title.split()) < 4 and len(title)<title_len:
            title += word + " "
    if title=="":
        title="No Title"
    return title

def generate_summary(text, summarizer, max_len=200):
    words = text.split()
    if len(words) < 40:
        return text.strip()

    summaries = []
    chunk_size = 400
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

def extract_keywords(text, kw_model, top_n=5):
    keywords = kw_model.extract_keywords(text, top_n=top_n, stop_words='english')
    return [kw for kw, _ in keywords]

def generate_metadata(text, summarizer, kw_model, author=None, subject=None, creation_date=None):
    # print(text)
    title = extract_title(text)
    summary = generate_summary(text, summarizer)
    keywords = extract_keywords(text, kw_model)

    metadata = {
        "title": title,
        "author": author or "Unknown",
        "subject": subject or summary[:60],  # Fallback subject: first 60 chars of summary
        "keywords": keywords,
        "creation_date": creation_date or datetime.today().strftime("%Y-%m-%d"),
        "summary": summary
    }
    return metadata
