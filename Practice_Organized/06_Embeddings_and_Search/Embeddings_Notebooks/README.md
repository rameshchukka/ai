# 🧪 Embedding & Retrieval Lab — JupyterLab Notebooks

A hands-on lab covering **embeddings, similarity search, ANN**, and visualisation  
across 5 real-world datasets: clinical, reviews, failure logs, support tickets, and research abstracts.

---

## 🗂️ Notebook Overview

| Notebook | Focus | Key Outputs |
|----------|-------|-------------|
| **NB1** — Datasets & Embeddings | Generate datasets, TF-IDF/LSA embeddings, t-SNE & UMAP visualisation | `embeddings_lsa.npy`, t-SNE plots, embedding health diagnostics |
| **NB2** — Similarity Methods | Cosine · Euclidean · Dot Product — math, code, benchmarks | Precision@K curves, score distributions, retrieval overlap |
| **NB3** — ANN & Retrieval | IVF, BallTree, full retrieval pipeline, MAP/MRR evaluation | ANN speed/accuracy charts, MAP heatmaps, summary dashboard |

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install numpy pandas scikit-learn matplotlib seaborn plotly umap-learn scipy

# Optional (for real sentence embeddings — MUCH better quality):
pip install sentence-transformers torch

# 2. Launch JupyterLab
jupyter lab

# 3. Run notebooks IN ORDER:
#    NB1 → NB2 → NB3
```

---

## 📦 Datasets Generated

| Domain | # Records | Categories | Notes |
|--------|-----------|------------|-------|
| **Clinical** | 500 | cardiology, neurology, oncology, endocrinology, respiratory | ICU-style notes |
| **Reviews** | ~500 | electronics, restaurants, hotels, software | +/−/neutral sentiment |
| **Failures** | 400 | mechanical, electrical, software, thermal, structural | Severity + downtime |
| **Support Tickets** | 400 | authentication, billing, performance, data, ui_ux | Priority P1–P4 |
| **Research** | 300 | machine_learning, climate_science, genomics, materials, epidemiology | Abstract style |

**Total: ~2,100 records**

---

## 🔬 What Each Similarity Metric Does

### Cosine Similarity
```
cos(θ) = (A · B) / (‖A‖ · ‖B‖)   ∈ [−1, 1]
```
- Measures **angular distance** between vectors
- Magnitude-invariant — document length doesn't bias it
- **Best for**: text embeddings, semantic search, normalised vectors
- **Use when**: "how similar in meaning" regardless of length

### Euclidean Similarity
```
d = √Σ(aᵢ − bᵢ)²   →   sim = 1 / (1 + d)
```
- Measures **straight-line distance** in embedding space
- Sensitive to magnitude — big vectors = far from origin
- **Best for**: when scale/magnitude carries semantic meaning
- **Use when**: failure severity, sensor readings, count-based embeddings

### Dot Product
```
A · B = Σ aᵢbᵢ   ∈ (−∞, +∞)
```
- Raw inner product — for unit vectors: **identical to cosine**
- Biases towards high-magnitude vectors when not normalised
- **Best for**: unit-norm embeddings (fastest at scale)
- **Use when**: vectors are guaranteed L2-normalised

---

## 📊 Visualisation Techniques

### t-SNE
- Collapses N-dimensional embeddings to 2D
- Preserves **local neighbourhood** structure
- Good for: identifying clusters, spotting outliers
- Limitation: distances between clusters not meaningful

### UMAP
- Also 2D reduction, but **preserves global structure** too
- Faster than t-SNE on large datasets
- Better for: validating that domain separation is real
- Requires: `pip install umap-learn`

### How to Use Them for Quality Checks
1. Color by **domain** → domains should form separate clouds
2. Color by **category** → within each domain, sub-clusters should appear
3. If everything blends together → embeddings are NOT encoding semantics
4. If clusters are clean → ready for ANN search

---

## 🔍 ANN Methods Compared

| Method | Build Time | Query Time | Recall@10 | Use When |
|--------|-----------|-----------|-----------|----------|
| Exact k-NN | O(1) | O(N·D) | 100% | <10K vecs, offline |
| IVF (k-means) | O(N·k) | O(N/n_clusters · nprobe · D) | 85–98% | 10K–10M vecs |
| BallTree | O(N log N) | O(D log N) | ~95% | 10K–500K, low-dim |
| HNSW (faiss/hnswlib) | O(N log N) | O(log N) | 95–99% | 1M+ vecs, production |

---

## 🔄 Upgrade to Real Embeddings

In NB1, replace the synthetic embeddings block with:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dim, fast
# or 'all-mpnet-base-v2' for higher quality (768-dim)

X = model.encode(df_all.text.tolist(), batch_size=64, show_progress_bar=True)
X = X / np.linalg.norm(X, axis=1, keepdims=True)  # L2-normalise
np.save("embedding_outputs/embeddings_dense.npy", X)
```

For clinical/medical data, use domain-specific models:
- `pritamdeka/S-PubMedBert-MS-MARCO` — medical literature
- `emilyalsentzer/Bio_ClinicalBERT` — clinical notes
- `sentence-transformers/all-MiniLM-L6-v2` — general purpose

---

## 📈 Key Results (Expected)

| Finding | What It Means |
|---------|---------------|
| Cosine wins on 4/5 domains | Text embeddings should always be normalised |
| Euclidean better for failures | Severity magnitude is semantically meaningful |
| Domain-specific > global embeddings | Specialised models beat general-purpose for narrow domains |
| IVF nprobe=4 gives ~92% recall at 3× speedup | ANN is worth it above ~50K records |

---

## 🛠️ Extending This Lab

1. **Add FAISS** for production-scale ANN:
   ```python
   import faiss
   index = faiss.IndexFlatIP(D)  # inner product (cosine for unit vecs)
   index.add(X.astype(np.float32))
   scores, indices = index.search(query.reshape(1,-1), k=10)
   ```

2. **Add metadata filtering** with FAISS IDMap or Weaviate/Qdrant

3. **Evaluate with your own labelled queries** — replace `precision_at_k` labels  
   with human-judged relevance for real NDCG/MAP scores

4. **Try hybrid search** — combine BM25 (keyword) + dense embeddings for best of both

---

*Generated for JupyterLab. Python 3.9+ required.*
