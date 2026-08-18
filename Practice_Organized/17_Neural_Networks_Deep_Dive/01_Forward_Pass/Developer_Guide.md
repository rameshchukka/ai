# Forward Pass — How a Neural Network Makes a Prediction — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

The forward pass is the sequence of computations that turns an input into a prediction: each layer applies weights, a bias, and a nonlinear activation function, then passes the result to the next layer.

## What You Will Learn

- A single neuron: weighted sum + bias + activation function
- Stacking neurons into layers, layers into a network
- Common activation functions: ReLU, sigmoid, tanh, softmax — and when to use each
- Matrix form of a forward pass (why it's fast on GPUs)
- How the final layer's shape/activation depends on the task (regression vs. binary vs. multiclass)

## Important Pointers / Tips

- **Tip:** ReLU is the default hidden-layer activation for most modern networks — simple and avoids vanishing gradients better than sigmoid/tanh.
- **Tip:** Use sigmoid only on a final binary-classification output; softmax for multiclass; nothing (linear) for regression.
- **Tip:** Track tensor shape through every layer on paper before coding — this prevents most bugs.
- **Tip:** A forward pass with random (untrained) weights should still run without shape errors — test this first.

## Common Pitfalls

- ⚠️ Forgetting an activation function between layers — a stack of purely linear layers collapses to one linear layer.
- ⚠️ Mismatched input/output feature dimensions between consecutive layers.

## Real-World Use Cases

- Every inference call in a deployed model is 'just' a forward pass — this is what runs in production.

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
