# PyTorch for Real-World Deep Learning — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

PyTorch represents data as tensors (like NumPy arrays, but GPU-capable and differentiable) and builds models as compositions of layers. The training loop — forward pass, loss, backward pass, optimizer step — is the pattern behind virtually every deep learning system.

## What You're About to Learn (and why it matters)

- Tensors: creation, shapes, dtype, GPU vs CPU
- Autograd: how `.backward()` computes gradients automatically
- `nn.Module`: building a network as layers + a forward() method
- Dataset & DataLoader: batching real data efficiently
- The training loop: forward → loss → backward → optimizer.step() → zero_grad()
- Overfitting/underfitting signals via train vs. validation loss
- Saving/loading model weights for reuse

## Before You Start — Quick Mindset Tips

- 💡 Always call `optimizer.zero_grad()` before `.backward()` — gradients accumulate otherwise.
- 💡 Use `model.train()` / `model.eval()` to correctly toggle dropout/batchnorm behavior.
- 💡 Wrap validation/inference code in `with torch.no_grad():` to save memory and time.
- 💡 Watch tensor shapes at every layer boundary — shape mismatches are the #1 PyTorch bug.

## Things That Trip People Up

- 🚧 Mixing `float32` and `float64` tensors causes dtype errors.
- 🚧 Forgetting `.item()` when logging a loss tensor (keeps the whole graph alive, memory leak).
- 🚧 Learning rate too high (loss explodes/NaNs) or too low (loss barely moves).
- 🚧 Not shuffling training data (`shuffle=True` in DataLoader) — the model learns order artifacts.

## Where You'll Actually Use This

- Image classification (e.g., defect detection, medical imaging triage)
- Tabular regression/classification (e.g., churn prediction, price prediction)
- Text classification with simple embedding + linear layers
- Transfer learning: fine-tuning a pretrained model on a small custom dataset

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
