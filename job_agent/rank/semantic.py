# rank/semantic.py

from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticScorer:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> np.ndarray:
        # normalize_embeddings=True makes dot == cosine for normalized vectors
        return self.model.encode(texts, normalize_embeddings=True)

    def similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        # dot product because embeddings are normalized
        return float(np.dot(a, b))
