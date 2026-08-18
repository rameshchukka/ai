# Recurrent Neural Networks (RNNs) & Sequence Models — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

RNNs process sequences step by step, carrying a hidden state forward so the network has 'memory' of earlier elements — the classical approach to text, time series, and other ordered data (now often superseded by Transformers for text, but still foundational and used for many time-series tasks).

## What You Will Learn

- The recurrence relation: hidden state updates as the sequence is processed
- Vanishing gradients over long sequences, and why LSTM/GRU were introduced
- LSTM/GRU gating intuition (what to keep, forget, output)
- Sequence-to-one vs. sequence-to-sequence architectures
- Where Transformers (attention) replaced RNNs, and where RNNs are still used

## Important Pointers / Tips

- **Tip:** For long sequences, prefer LSTM/GRU over a vanilla RNN — they handle long-range dependencies far better.
- **Tip:** Pad/truncate sequences to a consistent length per batch, and mask padding in the loss.
- **Tip:** For most modern NLP tasks, a pretrained Transformer will outperform an RNN you train from scratch — RNNs remain strong for smaller time-series problems.

## Common Pitfalls

- ⚠️ Not masking padded timesteps, letting the model learn from meaningless padding.
- ⚠️ Expecting a vanilla RNN to remember information from very early in a long sequence.

## Real-World Use Cases

- Time-series forecasting (demand, sensor data)
- Sequence tagging tasks and historically, language modeling/translation (now largely Transformer-based)

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
