import os
from typing import List, Dict, Any, Optional
from app.config import settings


class EmbeddingService:
    """
    Embedding service for semantic retrieval layer.
    Gracefully falls back to structured filtering when pgvector or remote embedding is offline.
    """

    def __init__(self):
        self.is_vector_enabled = settings.USE_PGVECTOR and bool(os.getenv("GROQ_API_KEY"))

    def compute_embedding(self, text: str) -> Optional[List[float]]:
        """Placeholder/Adapter for generating vector embeddings."""
        if not self.is_vector_enabled:
            return None
        # If active, returns dense vector
        return None

    def semantic_rank(self, query: str, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank items semantically based on query tokens and tags/descriptions.
        """
        if not items:
            return items
            
        tokens = [t.lower() for t in query.replace(",", " ").split() if len(t) > 2]
        scored = []
        for item in items:
            text_corpus = f"{item.get('name', '')} {item.get('category', '')} {item.get('description', '')} {' '.join(item.get('tags', []))}".lower()
            match_score = sum(1 for tok in tokens if tok in text_corpus)
            scored.append((match_score, item))
            
        scored.sort(key=lambda x: x[0], reverse=True)
        return [it for _, it in scored]


embedding_service = EmbeddingService()
