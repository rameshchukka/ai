# 🧬 Transformers & Attention: Zero to Hero — Guided Lab

The architecture behind every modern LLM, built from raw NumPy math with nothing hidden: tokenization, embeddings, positional encoding, Q/K/V, scaled dot-product attention, multi-head attention, residuals + layer norm, causal masking, and a working mini-GPT text generator.

## The teaching format (every chapter)
- 📖 **Theory** (detailed) — the concept explained properly, not just name-dropped
- 🧠 **Mental model** — the intuition to hold in your head
- 🖼️ **ASCII diagram** — a visual of how it fits together
- 🔬 **Worked example** — runnable code you execute and read
- ⚡ **Pro tips** and ⚠️ **Common traps** — what actually trips people up
- ✏️ **Your Turn** exercise → ✅ **Solution** (revealed right after)

## Chapters
1. Why attention? The problem with older sequence models
2. Tokenization & embeddings
3. Positional encoding
4. The attention mechanism, step by step (Q, K, V)
5. Scaled dot-product attention (the formula)
6. Multi-head attention
7. The Transformer block (residuals, layer norm, feed-forward)
8. Causal masking (why GPT can't peek ahead)
9. From logits to text: the generation loop
10. 🏆 Capstone: a tiny GPT-style text generator

## Requirements
```
pip install numpy
```

Weights are random (untrained), so capstone output is grammatically loose — the point is the exact mechanics, which are identical to real trained LLMs.

Work top to bottom. Attempt every ✏️ exercise before opening its ✅ solution, and finish with
the 🏆 capstone.
