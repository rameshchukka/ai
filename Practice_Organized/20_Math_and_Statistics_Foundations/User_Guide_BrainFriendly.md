# Math & Statistics Foundations for AI/ML — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

Every ML/AI technique in this course rests on a small set of math tools: vectors/matrices (linear algebra), the language of uncertainty (probability & statistics), rates of change (calculus), and rigorous ways to decide if a change actually worked (A/B testing). You don't need a math degree — you need working fluency with these specific pieces.

## What You're About to Learn (and why it matters)

- Vectors, matrices, dot products, and matrix multiplication as data transformations
- Eigenvalues/eigenvectors intuition (used in PCA, stability analysis)
- Probability distributions (normal, binomial, Poisson) and when each shows up in real data
- Bayes' theorem and updating beliefs with evidence
- Hypothesis testing (t-test), p-values, and confidence intervals
- Gradients and partial derivatives as 'the direction of steepest increase'
- A/B testing: sample size, statistical significance, and common pitfalls

## Before You Start — Quick Mindset Tips

- 💡 Think of a matrix as a function that transforms vectors — that mental model unlocks most of linear algebra's use in ML.
- 💡 A p-value answers 'how surprising is this result if there's really no effect' — it's not the probability the hypothesis is true.
- 💡 Always compute a confidence interval alongside a point estimate; a single number hides your uncertainty.
- 💡 For A/B tests, compute required sample size *before* running the test, not after peeking at results.

## Things That Trip People Up

- 🚧 Peeking at A/B test results early and stopping as soon as they look significant (inflates false-positive rate).
- 🚧 Confusing correlation with causation when interpreting statistical relationships.
- 🚧 Treating p < 0.05 as 'proven true' rather than 'unlikely under the null hypothesis, given this sample'.

## Where You'll Actually Use This

- PCA for dimensionality reduction (uses eigenvectors)
- A/B testing a new UI, pricing, or model version before full rollout
- Understanding why gradient descent in a neural network is literally following the negative gradient
- Statistical significance testing for experiment results in any data-driven product

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
