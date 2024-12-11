import pdfplumber
from PyPDF2 import PdfReader

def extract_content_from_pdf(file_path: str):
    text_content = []
    tables = []
    
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text_content.append(page.extract_text())
            tables.extend(page.extract_tables())
    
    return {"text": text_content, "tables": tables}

def extract_content_from_txt(file_path: str):
    with open(file_path, "r") as f:
        text_content = f.readlines()
    return {"text": text_content, "tables": []}
