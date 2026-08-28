# Phase 3 — Embeddings

## What embeddings are (recap)
Dense vectors such that semantically similar text produces vectors that are
close together by some distance metric. The geometry is learned, not designed —
no single dimension has human-readable meaning.

## Similarity metrics
| Metric | Intuition | Notes |
|---|---|---|
| Cosine similarity | Angle between vectors, ignores magnitude | Most common for text; range [-1, 1] |
| Euclidean distance | Straight-line distance | Sensitive to magnitude/normalization |
| Dot product | Magnitude-weighted similarity | Equivalent to cosine if vectors are unit-normalized |

## Embedding models — in-house vs Hugging Face
| Model | Source | Dimension (typical) | Notes |
|---|---|---|---|
| Jina embeddings v3 | Your in-house stack (`MODEL_JINA`) | 1024 | No external dependency — default choice |
| BAAI/bge (e.g. `bge-large-en-v1.5`) | Hugging Face download | 1024 | Strong general-purpose open embedding model, widely used as a benchmark reference |
| Nomic Embed | Hugging Face download | 768 | Notable for being trained with a contrastive objective specifically tuned for retrieval |
| Sentence Transformers (e.g. `all-MiniLM-L6-v2`) | Hugging Face download | 384 | Smaller/faster, common default in tutorials — lower quality than the above at the same compute budget |
| OpenAI embeddings (e.g. `text-embedding-3-small`) | OpenAI API (paid, not HF) | 1536 | No local download at all — pure API call, requires an API key |

Per your go-ahead, this phase's worksheet downloads and runs the three HF models
above directly (`pip install sentence-transformers`, models pulled from the Hub
on first use) — no workaround needed, since you're fine with HF dependency here.

## Why model choice changes your Chroma collection design
**Critical rule: one collection = one embedding model.** Mixing vectors from two
different models (or even two versions of the same model) in one collection
silently breaks similarity search — the geometries aren't comparable. If you want
to compare Jina vs BGE vs MiniLM, that means **three separate Chroma collections**,
not three sets of vectors in one collection.

## Teaser problem
> You want to A/B test whether BGE or Jina gives better retrieval for your
> corpus. A teammate suggests embedding everything once with BGE, once with
> Jina, and storing both sets of vectors in the same Chroma collection with a
> metadata field saying which model made which vector, so you can filter by
> model at query time. Why won't this work?

**Solution:** a single Chroma collection has one HNSW index built around one
vector space's geometry (and typically one fixed dimension). Storing
differently-shaped or differently-scaled vectors together breaks the index's
distance computations — a query embedded with Jina compared against a
BGE-produced vector isn't measuring anything meaningful, even if you filter by
metadata afterward, because the *search itself* (which happens before any
metadata filter) is already comparing incompatible vectors. The fix: separate
collections per model, query each independently, and compare results
side-by-side. See the worksheet for this comparison done correctly.
