"""
retrieve.py
Week 15 - Part A, Step 4: Basic retrieval

Embeds a query the same way documents were embedded, searches the ChromaDB
collection, and returns the top-k most similar chunks with their similarity
scores. Includes a top-k=1 vs top-k=5 comparison on known-answer queries.

Run: python retrieve.py
Requires: you've already run `python ingest.py` at least once.
"""

import chromadb
from chromadb.utils import embedding_functions

COLLECTION_NAME = "policy_docs"
DB_PATH = "./chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# TODO: these are 5 queries you already know the answer to (since you wrote
# the docs) - use them to sanity-check retrieval quality. Add your own if useful.
KNOWN_ANSWER_QUERIES = [
    "How long do I have to get a refund on an unopened item?",
    "Can I get express shipping on an international order?",
    "How much does an extended warranty cost per year?",
    "When does a ticket need to go to a Tier 2 specialist?",
    "What happens if my payment fails?",
]


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    return client.get_collection(name=COLLECTION_NAME, embedding_function=embed_fn)


def retrieve(query: str, top_k: int = 5) -> list:
    """Returns a list of {"text", "source", "section", "distance"} dicts, best match first."""
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=top_k)

    hits = []
    for text, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        hits.append({"text": text, "source": meta["source"], "section": meta["section"], "distance": dist})
    return hits


def print_hits(hits: list):
    for i, h in enumerate(hits, start=1):
        print(f"  {i}. [{h['source']} | distance={h['distance']:.4f}] {h['text'][:100]}...")


if __name__ == "__main__":
    for query in KNOWN_ANSWER_QUERIES:
        print(f"\n=== Query: {query!r} ===")

        print("-- top-k=1 --")
        print_hits(retrieve(query, top_k=1))

        print("-- top-k=5 --")
        print_hits(retrieve(query, top_k=5))
