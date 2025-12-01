import pandas as pd
import io
from PyPDF2 import PdfReader

def read_file(filename: str, file_bytes: bytes) -> str:
    if filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(file_bytes))
        return df.to_string()

    elif filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(file_bytes))
        return df.to_string()

    elif filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    else:
        return "Unsupported file format"
