import os
from PyPDF2 import PdfReader


def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf(path):
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def load_file(path):

    if path.endswith(".txt"):
        return load_txt(path)

    if path.endswith(".pdf"):
        return load_pdf(path)

    raise ValueError("Unsupported file type")