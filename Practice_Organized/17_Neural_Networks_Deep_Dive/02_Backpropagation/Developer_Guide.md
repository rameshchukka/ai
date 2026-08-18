# Backpropagation — How a Neural Network Learns — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

Backpropagation computes how much each weight contributed to the error (the gradient), using the chain rule, working backward from the loss. The optimizer then nudges each weight to reduce that error.

## What You Will Learn

- Loss functions: MSE for regression, cross-entropy for classification
- The chain rule intuition: how error 'flows backward' through layers
- Gradient descent and the role of the learning rate
- Why deep networks can suffer vanishing/exploding gradients
- How PyTorch's autograd automates this (`.backward()`, `.grad`)

## Important Pointers / Tips

- **Tip:** You rarely hand-derive gradients in practice — but understanding the chain-rule intuition helps you debug training issues.
- **Tip:** If loss becomes NaN, suspect learning rate too high or exploding gradients — try gradient clipping or a lower LR.
- **Tip:** If loss barely moves, suspect learning rate too low, vanishing gradients, or a bug in the loss/label pairing.
- **Tip:** Plot the training loss curve every time — it's the single most informative debugging tool.

## Common Pitfalls

- ⚠️ Forgetting `optimizer.zero_grad()` — gradients silently accumulate across batches.
- ⚠️ Using the wrong loss function for the task (e.g., MSE for classification).

## Real-World Use Cases

- This is literally what 'training a model' means — every framework's `.fit()` or training loop is doing this.

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
