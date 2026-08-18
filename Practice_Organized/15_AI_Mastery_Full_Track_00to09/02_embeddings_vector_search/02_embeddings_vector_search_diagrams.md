# Module 2 — Diagrams

## 1. Vector space, stylized 2D view

```
        y
        ^
        |        * "RAG combines retrieval..."
        |      *   "Retrieval-augmented generation..."
        |
        |                          * "12 * 7 = 84"
        |                          *  "calculator tool use"
        |
        +---------------------------------------> x
              (semantically similar texts land near each other;
               unrelated texts land far apart, in whatever
               directions the model learned during training)
```

## 2. Bi-encoder vs cross-encoder data flow

```
 BI-ENCODER (fast, used for searching millions of docs)
 ─────────────────────────────────────────────────────
   query  -> [Embedding Model] -> vector_q   ─┐
                                                ├─> cosine_sim(vector_q, vector_d)
   doc    -> [Embedding Model] -> vector_d   ─┘     (precompute vector_d ahead of time!)


 CROSS-ENCODER (slow, accurate, used only to RERANK a small top-k)
 ───────────────────────────────────────────────────────────────
   [query + doc together] -> [Cross-Encoder Model] -> relevance_score
   (must run once per query-doc PAIR — can't precompute)
```

## 3. Index type hierarchy

```
                    Vector Index
                         |
        ┌────────────────┼────────────────┐
        v                v                v
      Flat             HNSW              IVF
   (brute-force)    (graph-based,     (cluster-then-
                     approximate)      search, approximate)
        |                |                |
   100% accurate    ~95-99% accurate  medium-high accuracy
   slow at scale     fast, default     lower memory than HNSW
                      in Chroma/FAISS   at very large scale
                      /pgvector
```

## 4. Where dimensionality reduction sits in your pipeline

```
  [1024-dim embeddings in Chroma]
              |
              v
   ┌─────────────────────┐
   │ PCA / t-SNE / UMAP   │   <- ONLY for visualization/debugging
   │ (reduce to 2D or 3D) │      never used for actual retrieval —
   └─────────────────────┘      retrieval always uses full-dim vectors
              |
              v
      scatter plot you can
      actually look at
```
