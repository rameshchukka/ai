# Math & Statistics Foundations for AI/ML — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

Every ML/AI technique in this course rests on a small set of math tools: vectors/matrices (linear algebra), the language of uncertainty (probability & statistics), rates of change (calculus), and rigorous ways to decide if a change actually worked (A/B testing). You don't need a math degree — you need working fluency with these specific pieces.

## What You Will Learn

- Vectors, matrices, dot products, and matrix multiplication as data transformations
- Eigenvalues/eigenvectors intuition (used in PCA, stability analysis)
- Probability distributions (normal, binomial, Poisson) and when each shows up in real data
- Bayes' theorem and updating beliefs with evidence
- Hypothesis testing (t-test), p-values, and confidence intervals
- Gradients and partial derivatives as 'the direction of steepest increase'
- A/B testing: sample size, statistical significance, and common pitfalls

## Important Pointers / Tips

- **Tip:** Think of a matrix as a function that transforms vectors — that mental model unlocks most of linear algebra's use in ML.
- **Tip:** A p-value answers 'how surprising is this result if there's really no effect' — it's not the probability the hypothesis is true.
- **Tip:** Always compute a confidence interval alongside a point estimate; a single number hides your uncertainty.
- **Tip:** For A/B tests, compute required sample size *before* running the test, not after peeking at results.
- **Tip:** Gradient = vector of partial derivatives = the direction that increases a function fastest; negative gradient is used for descent.

## Common Pitfalls

- ⚠️ Peeking at A/B test results early and stopping as soon as they look significant (inflates false-positive rate).
- ⚠️ Confusing correlation with causation when interpreting statistical relationships.
- ⚠️ Treating p < 0.05 as 'proven true' rather than 'unlikely under the null hypothesis, given this sample'.

## Real-World Use Cases

- PCA for dimensionality reduction (uses eigenvectors)
- A/B testing a new UI, pricing, or model version before full rollout
- Understanding why gradient descent in a neural network is literally following the negative gradient
- Statistical significance testing for experiment results in any data-driven product

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
