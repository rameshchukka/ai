# Module 2 — Embeddings & Vector Search

## 1. What an embedding actually is
A dense vector (e.g. 1024 floats for Jina-v3) such that semantically similar
texts produce vectors that are *close together* by some distance metric. The
model learns this geometry during training — there's no human-designed meaning
to any single dimension.

## 2. Distance metrics
| Metric | Formula intuition | Notes |
|---|---|---|
| Cosine similarity | angle between vectors, ignores magnitude | Most common for text embeddings; range [-1, 1] |
| Euclidean (L2) | straight-line distance | Sensitive to magnitude; use if vectors aren't normalized |
| Dot product | magnitude-weighted similarity | Equivalent to cosine if vectors are unit-normalized |

**Practical bug source:** if your embeddings aren't normalized and your vector
DB defaults to dot product, you'll get distance-ranking distortions. Check
what metric your vector DB uses by default and whether your embedding model's
output is pre-normalized.

## 3. Bi-encoder vs cross-encoder
- **Bi-encoder** (e.g. Jina): embeds query and document *separately*, compares
  vectors. Fast — this is what makes large-scale retrieval feasible.
- **Cross-encoder**: feeds query+document *together* through one model,
  outputs a relevance score directly. Much more accurate, but O(n) cost per
  query (can't precompute) — this is why cross-encoders are used for
  **reranking** a small top-k, never for searching a whole corpus (Module 3).

## 4. Dimensionality reduction for visualization
| Method | Preserves | Speed | Use when |
|---|---|---|---|
| PCA | Global linear structure, variance | Fast | Quick sanity check, large datasets |
| t-SNE | Local neighborhood structure | Slow | Small-medium datasets, want tight visual clusters |
| UMAP | Local + some global structure | Medium | Good general-purpose default, scales better than t-SNE |

PCA is what you've been using so far (notebook 01, Chroma Navigator) — it's
the right default. Reach for UMAP/t-SNE when PCA's 2D projection looks like
one undifferentiated blob and you suspect there IS structure PCA's linearity
is flattening out.

## 5. Vector index types
| Index | Search | Accuracy | Build cost | Use when |
|---|---|---|---|---|
| Flat (brute-force) | Exact, compares every vector | 100% | None | Small corpora (<100K), correctness-critical |
| HNSW | Approximate, graph-based | High (~95-99%) | Moderate | Most production use cases — Chroma/FAISS/pgvector all support it |
| IVF | Approximate, clusters then searches | Medium-high | Lower than HNSW | Very large corpora, memory-constrained |

## 6. Vector DB landscape
| DB | Type | Hosting | Best for |
|---|---|---|---|
| Chroma | Embedded or server | Local/self-hosted | Prototyping, small-medium apps, simplicity |
| FAISS | Library, not a DB | Embedded only | Pure search speed, no metadata filtering needed |
| pgvector | Postgres extension | Self-hosted/managed Postgres | Want vector + relational in one transactional system |
| Pinecone | Managed cloud service | Cloud only | Production scale, don't want to run infra |
| Milvus | Distributed vector DB | Self-hosted or cloud | Very large scale, need horizontal scaling |

## Teaser problem
> Your top-k retrieval results look almost random — barely related to the
> query. The embedding model and chunking both look fine in isolation. What's
> the most common cause?

**Solution:** a metric/normalization mismatch (section 2) — e.g., the index
was built assuming cosine similarity but is configured for dot product on
un-normalized vectors, so "distance" no longer correlates with semantic
similarity. Second most common cause: query and documents were embedded with
*different* embedding models or different versions of the same model. See
the worksheet notebook in this folder for a reproduction of this bug and the fix.
