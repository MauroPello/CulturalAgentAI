import os
import docx
import pypdf
import pandas as pd
from typing import Callable, Dict

def _load_pdf(file_path: str) -> str:
    """Loads text from a PDF file."""
    text = ""
    reader = pypdf.PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def _load_docx(file_path: str) -> str:
    """Loads text from a DOCX file."""
    text = ""
    document = docx.Document(file_path)
    for para in document.paragraphs:
        text += para.text + "\n"
    return text

def _load_excel(file_path: str) -> str:
    """Loads text from an Excel file (XLSX/XLS)."""
    text = ""
    xls = pd.ExcelFile(file_path)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df.fillna("", inplace=True)
        if not df.empty:
            text += f"--- Sheet: {sheet_name} ---\n"
            text += df.to_string(index=False) + "\n\n"
    return text

def _load_txt(file_path: str) -> str:
    """Loads text from a plain text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

LOADER_MAPPING: Dict[str, Callable[[str], str]] = {
    ".pdf": _load_pdf,
    ".docx": _load_docx,
    ".xlsx": _load_excel,
    ".xls": _load_excel,
    ".txt": _load_txt,
}

def load_document_text(file_path: str, original_filename: str) -> str:
    """
    Detects file type from the original filename and extracts text using the appropriate loader.
    """
    _, file_extension = os.path.splitext(original_filename)
    ext_lower = file_extension.lower()

    if ext_lower not in LOADER_MAPPING:
        raise ValueError(f"Unsupported file type: {ext_lower}")

    loader_func = LOADER_MAPPING[ext_lower]
    
    try:
        return loader_func(file_path)
    except Exception as e:
        raise RuntimeError(f"Error processing file '{original_filename}': {e}")
