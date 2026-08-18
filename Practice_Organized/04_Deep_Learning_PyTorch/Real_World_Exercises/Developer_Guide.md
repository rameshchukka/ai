# PyTorch for Real-World Deep Learning — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

PyTorch represents data as tensors (like NumPy arrays, but GPU-capable and differentiable) and builds models as compositions of layers. The training loop — forward pass, loss, backward pass, optimizer step — is the pattern behind virtually every deep learning system.

## What You Will Learn

- Tensors: creation, shapes, dtype, GPU vs CPU
- Autograd: how `.backward()` computes gradients automatically
- `nn.Module`: building a network as layers + a forward() method
- Dataset & DataLoader: batching real data efficiently
- The training loop: forward → loss → backward → optimizer.step() → zero_grad()
- Overfitting/underfitting signals via train vs. validation loss
- Saving/loading model weights for reuse

## Important Pointers / Tips

- **Tip:** Always call `optimizer.zero_grad()` before `.backward()` — gradients accumulate otherwise.
- **Tip:** Use `model.train()` / `model.eval()` to correctly toggle dropout/batchnorm behavior.
- **Tip:** Wrap validation/inference code in `with torch.no_grad():` to save memory and time.
- **Tip:** Watch tensor shapes at every layer boundary — shape mismatches are the #1 PyTorch bug.
- **Tip:** Normalize/scale your inputs; unscaled inputs are a common cause of a model that won't learn.
- **Tip:** Start with a tiny subset of data and confirm the model can overfit it — a fast sanity check.

## Common Pitfalls

- ⚠️ Mixing `float32` and `float64` tensors causes dtype errors.
- ⚠️ Forgetting `.item()` when logging a loss tensor (keeps the whole graph alive, memory leak).
- ⚠️ Learning rate too high (loss explodes/NaNs) or too low (loss barely moves).
- ⚠️ Not shuffling training data (`shuffle=True` in DataLoader) — the model learns order artifacts.

## Real-World Use Cases

- Image classification (e.g., defect detection, medical imaging triage)
- Tabular regression/classification (e.g., churn prediction, price prediction)
- Text classification with simple embedding + linear layers
- Transfer learning: fine-tuning a pretrained model on a small custom dataset

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
