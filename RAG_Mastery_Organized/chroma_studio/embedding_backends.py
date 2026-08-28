"""
embedding_backends.py
=====================
Two interchangeable embedding sources, both exposing the SAME interface Chroma
expects (a callable that takes a list of strings and returns a list of vectors).

1. JinaHostedEmbedding   -> your in-house hosted Jina endpoint (no HuggingFace)
2. LocalSTEmbedding      -> a locally-downloaded model via sentence-transformers
                            (e.g. a Jina model you downloaded to disk, or MiniLM)

Chroma 1.5.9 accepts an embedding_function that implements __call__(self, input)
-> list[list[float]]. Both classes below follow that contract, so either can be
passed straight into get_or_create_collection(embedding_function=...).

IMPORTANT (matches your real inhouse_llm.py): the hosted Jina endpoint is
OpenAI-style: POST {base_url}/embeddings with body
{"input": [...], "dimension": 1024, "embedding_type": "float"}, and the response
is {"data": [{"embedding": [...]}, ...]}.
"""

from typing import List


class JinaHostedEmbedding:
    """Calls your in-house hosted Jina embedding endpoint over HTTP.
    No HuggingFace, no local model download."""

    def __init__(self, base_url: str, api_key: str, dimension: int = 1024, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.dimension = dimension
        self.timeout = timeout
        import requests  # imported here so the module still loads if requests is missing
        self._requests = requests

    def name(self) -> str:
        # Chroma 1.5.9 calls .name() on embedding functions for its metadata.
        return f"jina_hosted_{self.dimension}"

    def __call__(self, input: List[str]) -> List[List[float]]:
        # Chroma passes a list of strings as `input`.
        if isinstance(input, str):
            input = [input]
        resp = self._requests.post(
            f"{self.base_url}/embeddings",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"input": input, "dimension": self.dimension, "embedding_type": "float"},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        return [item["embedding"] for item in data["data"]]


class LocalSTEmbedding:
    """Uses a locally-downloaded sentence-transformers model. If the model isn't
    cached locally, sentence-transformers will TRY to download it from HuggingFace
    -- which your org blocks -- so download it once on an unblocked network first,
    or point model_name_or_path at a local folder."""

    def __init__(self, model_name_or_path: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(model_name_or_path)
        self._model_name = model_name_or_path

    def name(self) -> str:
        safe = self._model_name.replace("/", "_").replace("\\", "_")
        return f"local_st_{safe}"

    def __call__(self, input: List[str]) -> List[List[float]]:
        if isinstance(input, str):
            input = [input]
        vectors = self._model.encode(list(input), convert_to_numpy=True)
        return vectors.tolist()


def build_embedder(source: str, **kwargs):
    """Factory used by the Streamlit app.
    source: "jina_hosted" or "local_st".
    """
    if source == "jina_hosted":
        return JinaHostedEmbedding(
            base_url=kwargs["base_url"],
            api_key=kwargs["api_key"],
            dimension=kwargs.get("dimension", 1024),
        )
    elif source == "local_st":
        return LocalSTEmbedding(model_name_or_path=kwargs.get("model_name_or_path", "all-MiniLM-L6-v2"))
    else:
        raise ValueError(f"Unknown embedding source: {source!r}")
