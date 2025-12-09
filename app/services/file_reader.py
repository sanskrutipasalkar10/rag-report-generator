import csv
import docx
import PyPDF2
from typing import Union


def extract_text(file_path: str) -> str:
    """
    Extracts text from PDF, DOCX, or CSV files.
    """

    file_path = str(file_path).lower()

    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_docx(file_path)

    elif file_path.endswith(".csv"):
        return extract_csv(file_path)

    else:
        raise ValueError("Unsupported file type")


def extract_pdf(file_path: str) -> str:
    text = ""
    with open(file_path, "rb") as pdf:
        reader = PyPDF2.PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def extract_docx(file_path: str) -> str:
    document = docx.Document(file_path)
    return "\n".join([para.text for para in document.paragraphs])


def extract_csv(file_path: str) -> str:
    rows = []
    with open(file_path, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            rows.append(", ".join(row))
    return "\n".join(rows)
