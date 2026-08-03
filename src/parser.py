import os

from pypdf import PdfReader
from docx import Document


def extract_text_from_txt(file_path):
    """Read text from a TXT resume."""
    
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_text_from_pdf(file_path):
    """Extract text from a PDF resume."""
    
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_docx(file_path):
    """Extract text from a DOCX resume."""
    
    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def get_resume_text(file_path):
    """Extract text from a resume based on its file extension."""
    
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".txt":
        return extract_text_from_txt(file_path)

    elif extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    else:
        raise ValueError(f"Unsupported file format: {extension}")
