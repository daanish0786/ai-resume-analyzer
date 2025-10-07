
from sentence_transformers import SentenceTransformer
import numpy as np

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def embed_single(text: str) -> np.ndarray:
    model = get_model()
    vec = model.encode([text], normalize_embeddings=True)[0]
    return vec
