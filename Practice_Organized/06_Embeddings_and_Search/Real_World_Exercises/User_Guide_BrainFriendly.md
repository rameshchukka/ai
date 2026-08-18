# Embeddings & Semantic Search — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

Embeddings turn text (or images) into vectors of numbers where 'meaning-similar' items end up close together in vector space. This powers semantic search, recommendation, deduplication, and is the backbone of RAG.

## What You're About to Learn (and why it matters)

- What an embedding is and how it differs from TF-IDF/keyword search
- Cosine similarity vs. Euclidean distance for comparing vectors
- Building a simple TF-IDF and BM25 keyword search baseline
- Building a semantic search index with embeddings
- Hybrid search: combining keyword + semantic signals
- Evaluating search quality (precision@k, recall@k)

## Before You Start — Quick Mindset Tips

- 💡 Normalize embedding vectors before cosine similarity for consistent scoring.
- 💡 Keyword search (BM25) still wins for exact terms (product codes, names) — hybrid is usually best.
- 💡 Chunk size matters: too small loses context, too large dilutes relevance — 200-500 tokens is a common start.
- 💡 Cache embeddings; recomputing them per query is wasteful and slow.

## Things That Trip People Up

- 🚧 Comparing embeddings from two different models — they don't share a vector space.
- 🚧 Forgetting to re-embed content after edits, leaving stale vectors in the index.
- 🚧 Using raw dot product for un-normalized vectors and misreading the scale.

## Where You'll Actually Use This

- 'Find similar documents/products' recommendation features
- Semantic FAQ / knowledge-base search
- Duplicate/near-duplicate content detection
- The retrieval step inside a RAG pipeline

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
