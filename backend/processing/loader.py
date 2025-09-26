import os
import pypdf
import docx
import pandas as pd
from fastapi import HTTPException

def load_document_text(file_path: str, original_filename: str) -> str:
    """Detects file type and extracts text using the appropriate loader."""
    _, file_extension = os.path.splitext(original_filename)
    text = ""

    try:
        if file_extension.lower() == ".pdf":
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
        
        elif file_extension.lower() == ".docx":
            document = docx.Document(file_path)
            for para in document.paragraphs:
                text += para.text + "\n"

        elif file_extension.lower() in [".xlsx", ".xls"]:
            xls = pd.ExcelFile(file_path)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                df.fillna("", inplace=True) # Replace NaN with empty strings
                text += f"--- Sheet: {sheet_name} ---\n"
                text += df.to_string(index=False) + "\n\n"
        
        elif file_extension.lower() == ".txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        
        else:
            # This will be caught by the endpoint, but good to have
            return None

    except Exception as e:
        # Raise an exception that the endpoint can catch
        raise RuntimeError(f"Error processing file {original_filename}: {e}")
        
    return text