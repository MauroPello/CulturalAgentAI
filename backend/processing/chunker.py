from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str) -> List[str]:
    """Splits a long text into smaller, semantically coherent chunks."""
    if not text:
        return []
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks