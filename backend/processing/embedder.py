from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

# Initialize the model. This will download it on the first run.
# 'all-MiniLM-L6-v2' is a good, fast, and lightweight starting model.
# It creates 384-dimensional vectors.
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu') # Specify CPU for broad compatibility
print("Embedding model loaded.")

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """Embeds a list of text chunks using a sentence-transformer model."""
    if not chunks:
        return []
    
    # The .encode() method runs the model on the chunks.
    embeddings = model.encode(chunks, convert_to_tensor=False)
    
    # Convert numpy arrays to lists for JSON serialization
    return [embedding.tolist() for embedding in embeddings]