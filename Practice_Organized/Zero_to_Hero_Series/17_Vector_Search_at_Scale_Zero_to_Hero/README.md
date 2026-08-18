# ⚡ Vector Search at Scale: Zero to Hero — Guided Lab

How production vector databases (FAISS, Pinecone, Chroma, Weaviate) actually search billions of vectors in milliseconds: IVF clustering, LSH hashing, HNSW graph search (the industry default), Product Quantization compression, and combined IVF+PQ — with the accuracy/speed tradeoffs made concrete through benchmarks.

## The teaching format (every chapter)
- 📖 **Theory** (detailed) — the concept explained properly, not just name-dropped
- 🧠 **Mental model** — the intuition to hold in your head
- 🖼️ **ASCII diagram** — a visual of how it fits together
- 🔬 **Worked example** — runnable code you execute and read
- ⚡ **Pro tips** and ⚠️ **Common traps** — what actually trips people up
- ✏️ **Your Turn** exercise → ✅ **Solution** (revealed right after)

## Chapters
1. Why brute-force doesn't scale
2. The accuracy/speed tradeoff: approximate search
3. Clustering-based search: IVF (Inverted File Index)
4. Locality-Sensitive Hashing (LSH)
5. Graph-based search: HNSW (the industry standard)
6. Product Quantization (compressing vectors)
7. Combining techniques: IVF + PQ
8. Evaluating ANN quality: recall@k vs. speed
9. Choosing an index for your use case
10. 🏆 Capstone: benchmark 3 index types on a larger corpus

## Requirements
```
pip install numpy scikit-learn
```

Prerequisite: the Embeddings & Search lab. All three benchmarked indexes (brute force, IVF, HNSW) achieve verified recall@5.

Work top to bottom. Attempt every ✏️ exercise before opening its ✅ solution, and finish with
the 🏆 capstone.
