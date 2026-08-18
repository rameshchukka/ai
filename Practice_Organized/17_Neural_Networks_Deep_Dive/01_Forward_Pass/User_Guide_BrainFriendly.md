# Forward Pass — How a Neural Network Makes a Prediction — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

The forward pass is the sequence of computations that turns an input into a prediction: each layer applies weights, a bias, and a nonlinear activation function, then passes the result to the next layer.

## What You're About to Learn (and why it matters)

- A single neuron: weighted sum + bias + activation function
- Stacking neurons into layers, layers into a network
- Common activation functions: ReLU, sigmoid, tanh, softmax — and when to use each
- Matrix form of a forward pass (why it's fast on GPUs)
- How the final layer's shape/activation depends on the task (regression vs. binary vs. multiclass)

## Before You Start — Quick Mindset Tips

- 💡 ReLU is the default hidden-layer activation for most modern networks — simple and avoids vanishing gradients better than sigmoid/tanh.
- 💡 Use sigmoid only on a final binary-classification output; softmax for multiclass; nothing (linear) for regression.
- 💡 Track tensor shape through every layer on paper before coding — this prevents most bugs.
- 💡 A forward pass with random (untrained) weights should still run without shape errors — test this first.

## Things That Trip People Up

- 🚧 Forgetting an activation function between layers — a stack of purely linear layers collapses to one linear layer.
- 🚧 Mismatched input/output feature dimensions between consecutive layers.

## Where You'll Actually Use This

- Every inference call in a deployed model is 'just' a forward pass — this is what runs in production.

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
