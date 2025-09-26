from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def chunk_text(text: str) -> List[str]:
    """Splits a long text into smaller, semantically coherent chunks."""
    if not text or not text.strip():
        return []
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return [chunk for chunk in chunks if chunk.strip()]