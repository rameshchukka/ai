# Machine Learning Fundamentals — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

Classical ML — the algorithms that predate/complement deep learning and still power most production systems (tabular data, smaller datasets, interpretability needs). Understanding these makes deep learning make more sense too.

## What You Will Learn

- Supervised vs. unsupervised vs. reinforcement learning
- The train/validation/test split and why it exists
- Linear & logistic regression as the simplest predictive models
- Decision trees & random forests (interpretable, strong tabular baselines)
- k-Nearest Neighbors and k-Means clustering
- Bias-variance tradeoff, overfitting/underfitting
- Evaluation metrics: accuracy, precision/recall/F1, ROC-AUC, RMSE/MAE
- Feature engineering & scaling

## Important Pointers / Tips

- **Tip:** Always start with a simple baseline model (e.g., logistic regression) before reaching for something complex.
- **Tip:** A model with 99% accuracy on an imbalanced dataset can still be useless — check precision/recall per class.
- **Tip:** Cross-validation gives a more reliable performance estimate than a single train/test split.
- **Tip:** Tree-based models (random forest, gradient boosting) are usually the strongest baseline on tabular data.
- **Tip:** Scale features for distance-based models (KNN, k-means, SVM) — tree models don't need it.

## Common Pitfalls

- ⚠️ Data leakage: information from the test set (or the future) sneaking into training.
- ⚠️ Evaluating only on training data and being surprised by poor real-world performance.
- ⚠️ Choosing accuracy as the only metric on an imbalanced classification problem.

## Real-World Use Cases

- Credit risk / churn prediction from tabular customer data
- Spam/fraud classification
- Customer segmentation via clustering
- Demand forecasting with regression

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
