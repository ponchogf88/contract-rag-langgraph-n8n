from typing import List
import numpy as np
from .models import Chunk, DocType

_model = None
_matrix = None
_chunks: List[Chunk] = []

def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        import os
        name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        _model = SentenceTransformer(name)
    return _model

def build_index(chunks: List[Chunk]) -> None:
    global _matrix, _chunks
    _chunks = chunks
    model = _get_model()
    vectors = model.encode([c.text for c in chunks], normalize_embeddings=True)
    _matrix = np.array(vectors)

def retrieve(query: str, doc_type: DocType, k: int = 4) -> List[Chunk]:
    if _matrix is None:
        raise RuntimeError("Index not built")
    model = _get_model()
    q = model.encode([query], normalize_embeddings=True)[0]
    scores = _matrix @ q
    ranked = sorted(zip(scores, _chunks), key=lambda x: float(x[0]), reverse=True)
    routed = [c for s, c in ranked if c.doc_type == doc_type][:k]
    if len(routed) < 2:
        routed = [c for s, c in ranked[:k]]
    for c, (s, _) in zip(routed, ranked):
        c.score = float(s)
    return routed
