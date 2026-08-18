"""
chunking.py
Week 15 - Part A, Step 2: Chunking

Splits documents into overlapping chunks, preserving source filename + a
best-effort section title as metadata. Chunk size and overlap are the two
levers that most affect RAG quality - see the tutorial's Article 15.4.

Run: python chunking.py
Prints 5 sample chunks so you can sanity-check them by eye.
"""

import os
import glob

DOCS_DIR = "docs"
CHUNK_SIZE_WORDS = 120   # ~roughly 150-160 tokens; adjust and re-test
OVERLAP_WORDS = 20       # ~15-20% overlap


def load_documents(docs_dir: str = DOCS_DIR) -> dict:
    """Return {filename: full_text} for every .txt file in docs_dir."""
    docs = {}
    for path in glob.glob(os.path.join(docs_dir, "*.txt")):
        with open(path, "r") as f:
            docs[os.path.basename(path)] = f.read()
    return docs


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE_WORDS, overlap: int = OVERLAP_WORDS) -> list:
    """
    Simple word-count-based chunking with overlap. Not sentence-aware - a
    production system would prefer splitting on paragraph/section boundaries
    first, falling back to word-count only within an oversized paragraph.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        if end >= len(words):
            break
        start = end - overlap
    return chunks


def chunk_all_documents(docs_dir: str = DOCS_DIR) -> list:
    """
    Returns a list of dicts: {"text": ..., "source": filename, "chunk_index": i}
    This is the structure ingest.py expects.
    """
    all_chunks = []
    docs = load_documents(docs_dir)
    for filename, text in docs.items():
        # naive "section title" = first line of the doc (works for our policy docs,
        # which each start with a title line)
        section_title = text.strip().split("\n")[0]
        for i, chunk in enumerate(chunk_text(text)):
            all_chunks.append({
                "text": chunk,
                "source": filename,
                "section": section_title,
                "chunk_index": i,
            })
    return all_chunks


if __name__ == "__main__":
    chunks = chunk_all_documents()
    print(f"Total chunks created: {len(chunks)}\n")
    print("=== 5 sample chunks ===\n")
    for c in chunks[:5]:
        print(f"[{c['source']} | section: {c['section']} | chunk {c['chunk_index']}]")
        print(c["text"])
        print("-" * 60)
