# Embeddings & Semantic Search — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

Embeddings turn text (or images) into vectors of numbers where 'meaning-similar' items end up close together in vector space. This powers semantic search, recommendation, deduplication, and is the backbone of RAG.

## What You Will Learn

- What an embedding is and how it differs from TF-IDF/keyword search
- Cosine similarity vs. Euclidean distance for comparing vectors
- Building a simple TF-IDF and BM25 keyword search baseline
- Building a semantic search index with embeddings
- Hybrid search: combining keyword + semantic signals
- Evaluating search quality (precision@k, recall@k)

## Important Pointers / Tips

- **Tip:** Normalize embedding vectors before cosine similarity for consistent scoring.
- **Tip:** Keyword search (BM25) still wins for exact terms (product codes, names) — hybrid is usually best.
- **Tip:** Chunk size matters: too small loses context, too large dilutes relevance — 200-500 tokens is a common start.
- **Tip:** Cache embeddings; recomputing them per query is wasteful and slow.
- **Tip:** Always eyeball your top-k results manually before trusting a metric.

## Common Pitfalls

- ⚠️ Comparing embeddings from two different models — they don't share a vector space.
- ⚠️ Forgetting to re-embed content after edits, leaving stale vectors in the index.
- ⚠️ Using raw dot product for un-normalized vectors and misreading the scale.

## Real-World Use Cases

- 'Find similar documents/products' recommendation features
- Semantic FAQ / knowledge-base search
- Duplicate/near-duplicate content detection
- The retrieval step inside a RAG pipeline

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
