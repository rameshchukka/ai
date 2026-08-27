"""
hybrid_search.py
Week 15 - Part A, Step 5 (stretch goal): Hybrid search

Combines BM25 keyword matching with vector similarity search. Pure semantic
search sometimes misses exact terms (dollar amounts, specific day counts,
policy names) that keyword search catches directly - this script lets you
compare both approaches side by side on the same queries.

Run: python hybrid_search.py
Requires: you've already run `python ingest.py` at least once.
"""

from rank_bm25 import BM25Okapi
from chunking import chunk_all_documents
from retrieve import retrieve, KNOWN_ANSWER_QUERIES, print_hits


def build_bm25_index():
    chunks = chunk_all_documents()
    tokenized_corpus = [c["text"].lower().split() for c in chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    return bm25, chunks


def bm25_search(query: str, bm25, chunks: list, top_k: int = 5) -> list:
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)
    ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)[:top_k]
    return [{"text": c["text"], "source": c["source"], "score": score} for score, c in ranked]


def print_bm25_hits(hits: list):
    for i, h in enumerate(hits, start=1):
        print(f"  {i}. [{h['source']} | bm25_score={h['score']:.4f}] {h['text'][:100]}...")


if __name__ == "__main__":
    bm25, chunks = build_bm25_index()

    for query in KNOWN_ANSWER_QUERIES:
        print(f"\n=== Query: {query!r} ===")

        print("-- Vector search (top-k=3) --")
        print_hits(retrieve(query, top_k=3))

        print("-- BM25 keyword search (top-k=3) --")
        print_bm25_hits(bm25_search(query, bm25, chunks, top_k=3))

    print(
        "\nTODO: Note any query above where BM25 and vector search disagreed on the "
        "top result, and which one was actually more relevant. This is what a "
        "production hybrid-search implementation combines (weighted score fusion) "
        "rather than picking one or the other."
    )
