# app/services/ingestion.py
import pandas as pd
import docx
from PyPDF2 import PdfReader
from pathlib import Path
from app.config import DATA_DIR

DATA_DIR.mkdir(parents=True, exist_ok=True)

async def save_uploaded_file(file) -> Path:
    out_path = DATA_DIR / file.filename
    contents = await file.read()
    with open(out_path, "wb") as f:
        f.write(contents)
    return out_path

def parse_csv(path: Path):
    df = pd.read_csv(path).astype(str)
    return df.apply(lambda row: " | ".join(row.values.tolist()), axis=1).tolist()

def parse_pdf(path: Path):
    reader = PdfReader(str(path))
    return [page.extract_text() or "" for page in reader.pages]

def parse_docx(path: Path):
    doc = docx.Document(str(path))
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    chunks = []
    start = 0
    text = text.replace("\n", " ").strip()
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
    return chunks

def ingest_file(path: Path):
    ext = path.suffix.lower()
    texts = []
    if ext == ".csv":
        texts = parse_csv(path)
    elif ext in (".xls", ".xlsx"):
        df = pd.read_excel(path).astype(str)
        texts = df.apply(lambda row: " | ".join(row.values.tolist()), axis=1).tolist()
    elif ext == ".pdf":
        texts = parse_pdf(path)
    elif ext in (".docx", ".doc"):
        texts = parse_docx(path)
    else:
        with open(path, "r", encoding="utf-8") as f:
            texts = chunk_text(f.read())

    final_chunks = []
    for t in texts:
        if len(t) > 1000:
            final_chunks.extend(chunk_text(t, chunk_size=800, overlap=100))
        else:
            final_chunks.append(t)
    return final_chunks
