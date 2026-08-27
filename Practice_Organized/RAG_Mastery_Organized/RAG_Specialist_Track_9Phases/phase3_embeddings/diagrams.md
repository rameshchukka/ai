# Phase 3 — Diagrams

## 1. Model landscape: in-house vs Hugging Face vs paid API

```
                    Embedding Models
                          |
        ┌─────────────────┼─────────────────┐
        v                 v                 v
   In-house          Hugging Face        Paid API
        |                 |                 |
   Jina (MODEL_JINA)  BAAI/bge          OpenAI embeddings
   no download,       Nomic Embed       no download,
   already             Sentence          needs API key,
   integrated          Transformers      costs per call
                       (all downloaded
                        on first use,
                        cached locally
                        after that)
```

## 2. Why mixing models in one collection breaks search

```
  Collection "docs" (built around Jina's 1024-dim geometry)
        |
        ├── doc_1 embedded with JINA   --> [0.21, -0.05, ..., 0.13]  (1024 dims)
        ├── doc_2 embedded with JINA   --> [0.18, -0.09, ..., 0.07]  (1024 dims)
        └── doc_3 embedded with BGE    --> [0.44,  0.12, ..., -0.3]  (1024 dims,
                                            SAME length, but a totally
                                            different, incompatible geometry)

  query embedded with JINA --> compared against doc_3's BGE vector
  "distance" computed, but it means NOTHING — the two vector spaces
  were never trained to be comparable to each other, even though the
  dimension count happens to match by coincidence.

  FIX: separate collections per model --------------------------
       collection "docs_jina"  <- only Jina vectors
       collection "docs_bge"   <- only BGE vectors
       query each independently, compare results side-by-side
```

## 3. Metric relationship (when vectors ARE normalized)

```
  unit-normalized vectors:  ||a|| = ||b|| = 1
        |
        v
  cosine_similarity(a, b) == dot_product(a, b)
        |
        v
  euclidean_distance(a, b) = sqrt(2 - 2*cosine_similarity(a, b))

  (this is why "just use dot product, it's faster" is a VALID
   shortcut ONLY if you've confirmed your vectors are normalized —
   the bug from Module 2 of the AI Mastery track, revisited here in
   a model-comparison context)
```
