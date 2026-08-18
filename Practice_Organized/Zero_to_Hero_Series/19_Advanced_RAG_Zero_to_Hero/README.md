# 🚀 Advanced RAG: Zero to Hero — Guided Lab

The techniques that separate a demo RAG system from a production-grade one: query rewriting/expansion, cross-encoder re-ranking, HyDE (Hypothetical Document Embeddings), multi-hop retrieval for compound questions, query routing, contextual compression, and self-correcting retrieval. Capstone verified on a real multi-hop question.

## The teaching format (every chapter)
- 📖 **Theory** (detailed) — the concept explained properly, not just name-dropped
- 🧠 **Mental model** — the intuition to hold in your head
- 🖼️ **ASCII diagram** — a visual of how it fits together
- 🔬 **Worked example** — runnable code you execute and read
- ⚡ **Pro tips** and ⚠️ **Common traps** — what actually trips people up
- ✏️ **Your Turn** exercise → ✅ **Solution** (revealed right after)

## Chapters
1. Where basic RAG breaks down
2. Query rewriting & expansion
3. Re-ranking with a cross-encoder
4. HyDE: Hypothetical Document Embeddings
5. Multi-hop retrieval
6. Query routing (choosing the right retrieval strategy)
7. Contextual compression
8. Self-correction: checking your own retrieval
9. Combining everything: an advanced RAG pipeline
10. 🏆 Capstone: an advanced RAG assistant on a multi-hop question

## Requirements
```
pip install --upgrade pip   # no external deps required
```

Prerequisite: the RAG lab and the Embeddings & Search lab. Builds directly on the basic retrieve-then-generate pipeline.

Work top to bottom. Attempt every ✏️ exercise before opening its ✅ solution, and finish with
the 🏆 capstone.
