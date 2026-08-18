# 🎯 Embedding Model Training: Zero to Hero — Guided Lab

How embedding models like Sentence-BERT and OpenAI's text-embedding-3 actually learn: contrastive loss, triplet loss, in-batch negatives (the efficiency trick behind large-scale training), a full PyTorch training loop for embeddings, retrieval-based evaluation, and hard negative mining. Capstone verified: 20% -> 100% top-1 accuracy after training.

## The teaching format (every chapter)
- 📖 **Theory** (detailed) — the concept explained properly, not just name-dropped
- 🧠 **Mental model** — the intuition to hold in your head
- 🖼️ **ASCII diagram** — a visual of how it fits together
- 🔬 **Worked example** — runnable code you execute and read
- ⚡ **Pro tips** and ⚠️ **Common traps** — what actually trips people up
- ✏️ **Your Turn** exercise → ✅ **Solution** (revealed right after)

## Chapters
1. What 'training an embedding' even means
2. Similarity targets: what should be close, what should be far
3. Contrastive loss (the core idea)
4. Triplet loss: anchor, positive, negative
5. In-batch negatives (how real models train efficiently)
6. Building a trainable embedding model in PyTorch
7. The training loop for embeddings
8. Evaluating embedding quality
9. Hard negative mining
10. 🏆 Capstone: train an embedding model on a real similarity task

## Requirements
```
pip install torch
```

Prerequisite: the PyTorch lab and the Embeddings & Search lab. This is how the embeddings you USED in those labs are actually built.

Work top to bottom. Attempt every ✏️ exercise before opening its ✅ solution, and finish with
the 🏆 capstone.
