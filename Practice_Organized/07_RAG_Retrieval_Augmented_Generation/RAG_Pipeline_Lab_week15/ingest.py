"""
ingest.py
Week 15 - Part A, Step 3: Embedding + vector store

Embeds every chunk from chunking.py using a local sentence-transformers model
(no API cost/calls needed for embeddings) and stores them in a local ChromaDB
collection along with their source metadata.

Run: python ingest.py
Creates a local ./chroma_db/ directory - this is gitignored (see .gitignore);
re-run this script any time you need to rebuild the index from docs/.

Note: for a persistent/production-style setup, swap chromadb.PersistentClient
below for your cloud provider's managed vector-search service instead - see
the Guided Labs doc for the AI Cloud Sandbox version of this step.
"""

import chromadb
from chromadb.utils import embedding_functions
from chunking import chunk_all_documents

COLLECTION_NAME = "policy_docs"
DB_PATH = "./chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # small, fast, runs locally - no API needed


def build_index():
    client = chromadb.PersistentClient(path=DB_PATH)

    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)

    # Drop and recreate so re-running this script always reflects the current docs/ folder
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(name=COLLECTION_NAME, embedding_function=embed_fn)

    chunks = chunk_all_documents()
    print(f"Embedding and storing {len(chunks)} chunks...")

    collection.add(
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"], "section": c["section"], "chunk_index": c["chunk_index"]} for c in chunks],
        ids=[f"{c['source']}::{c['chunk_index']}" for c in chunks],
    )

    print(f"Done. Collection '{COLLECTION_NAME}' now has {collection.count()} chunks.")
    return collection


if __name__ == "__main__":
    build_index()
