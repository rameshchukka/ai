from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """Create text embeddings locally with a HuggingFace sentence-transformers model.

    Running the model on this machine means NO API calls and NO rate limits,
    unlike a cloud embedding service. The default model 'all-mpnet-base-v2'
    returns 768-number vectors (same size as Gemini's text-embedding-004), so
    the Neo4j vector index does not need to change.
    """

    def __init__(self, model: str = "all-mpnet-base-v2"):
        # Loads the model once. The first run downloads it (a few hundred MB)
        # and caches it on disk; later runs load it instantly from the cache.
        self.model = SentenceTransformer(model)

    def generate(self, text: str) -> List[float]:
        # encode() returns a numpy array. normalize_embeddings=True scales each
        # vector to length 1, so a dot product equals cosine similarity (which
        # is what our Neo4j search compares). .tolist() makes it a plain list.
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

    # The two methods below exist so the rest of the app can stay the same.
    # all-mpnet uses one model for both documents and queries, so they are
    # identical here (a cloud model sometimes treats them differently).
    def generate_document_embedding(self, text: str) -> List[float]:
        return self.generate(text)

    def generate_query_embedding(self, text: str) -> List[float]:
        return self.generate(text)
