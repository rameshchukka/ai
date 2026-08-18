# Backpropagation — How a Neural Network Learns — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

Backpropagation computes how much each weight contributed to the error (the gradient), using the chain rule, working backward from the loss. The optimizer then nudges each weight to reduce that error.

## What You're About to Learn (and why it matters)

- Loss functions: MSE for regression, cross-entropy for classification
- The chain rule intuition: how error 'flows backward' through layers
- Gradient descent and the role of the learning rate
- Why deep networks can suffer vanishing/exploding gradients
- How PyTorch's autograd automates this (`.backward()`, `.grad`)

## Before You Start — Quick Mindset Tips

- 💡 You rarely hand-derive gradients in practice — but understanding the chain-rule intuition helps you debug training issues.
- 💡 If loss becomes NaN, suspect learning rate too high or exploding gradients — try gradient clipping or a lower LR.
- 💡 If loss barely moves, suspect learning rate too low, vanishing gradients, or a bug in the loss/label pairing.
- 💡 Plot the training loss curve every time — it's the single most informative debugging tool.

## Things That Trip People Up

- 🚧 Forgetting `optimizer.zero_grad()` — gradients silently accumulate across batches.
- 🚧 Using the wrong loss function for the task (e.g., MSE for classification).

## Where You'll Actually Use This

- This is literally what 'training a model' means — every framework's `.fit()` or training loop is doing this.

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
