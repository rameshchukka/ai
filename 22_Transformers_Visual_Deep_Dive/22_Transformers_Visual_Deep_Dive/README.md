# 👁️ Transformers Visually: RNN vs Attention, Real Heatmaps, Training vs Inference

A concepts-first companion to 11_Transformers_Attention_Zero_to_Hero: why Transformers replaced RNNs (measured, not claimed), real attention-weight heatmaps on real sentences, multi-head specialization rendered per-head, and the training-vs-inference behavioral split (teacher forcing vs KV-cached autoregressive generation). Capstone verified: from-scratch multi-head attention matches PyTorch's real nn.MultiheadAttention to 1e-7.

## The teaching format (every chapter)
- 📖 **Theory** (detailed) — the concept explained properly, not just name-dropped
- 🧠 **Mental model** — the intuition to hold in your head
- 🖼️ **ASCII diagram** — a visual of how it fits together
- 🔬 **Worked example** — runnable code you execute and read
- ⚡ **Pro tips** and ⚠️ **Common traps** — what actually trips people up
- ✏️ **Your Turn** exercise → ✅ **Solution** (revealed right after)

## Chapters
1. Why Transformers replaced RNNs -- build both, watch the difference happen
2. How it works end-to-end -- real matrix shapes, visualized at every step
3. Multi-head attention, deep dive -- render each head's pattern separately
4. Why attention works -- a real coreference example, visualized
5. Training-time behavior -- teacher forcing, one parallel pass
6. Inference-time behavior -- autoregressive generation, KV-caching
7. 🏆 Capstone: verify your attention matches PyTorch's real nn.MultiheadAttention exactly

## Requirements
```
pip install numpy matplotlib torch
```

Prerequisite: 11_Transformers_Attention_Zero_to_Hero (Q/K/V, the attention formula) and ideally 21_Micrograd_Visual_Backprop. Every numerical claim in this lab (RNN information dilution, KV-cache speedup, PyTorch match) was measured directly, not asserted.

Work top to bottom. Attempt every ✏️ exercise before opening its ✅ solution, and finish with
the 🏆 capstone.
