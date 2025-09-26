import torch
from typing import List
from sentence_transformers import SentenceTransformer

MODEL_NAME = 'all-MiniLM-L6-v2'

model = None

def _get_embedding_model():
    """
    Initializes and returns the sentence transformer model, loading it only once.
    Automatically detects and uses a GPU if available.
    """
    global model
    if model is None:
        print("Initializing embedding model...")

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {device}")
        
        model = SentenceTransformer(MODEL_NAME, device=device)
        print("Embedding model loaded.")
    return model

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """Embeds a list of text chunks using a sentence-transformer model."""
    if not chunks:
        return []
    
    embedding_model = _get_embedding_model()
    embeddings = embedding_model.encode(chunks, convert_to_tensor=False)
    
    return [embedding.tolist() for embedding in embeddings]
