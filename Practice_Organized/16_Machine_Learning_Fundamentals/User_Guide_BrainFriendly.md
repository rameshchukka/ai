# Machine Learning Fundamentals — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

Classical ML — the algorithms that predate/complement deep learning and still power most production systems (tabular data, smaller datasets, interpretability needs). Understanding these makes deep learning make more sense too.

## What You're About to Learn (and why it matters)

- Supervised vs. unsupervised vs. reinforcement learning
- The train/validation/test split and why it exists
- Linear & logistic regression as the simplest predictive models
- Decision trees & random forests (interpretable, strong tabular baselines)
- k-Nearest Neighbors and k-Means clustering
- Bias-variance tradeoff, overfitting/underfitting
- Evaluation metrics: accuracy, precision/recall/F1, ROC-AUC, RMSE/MAE
- Feature engineering & scaling

## Before You Start — Quick Mindset Tips

- 💡 Always start with a simple baseline model (e.g., logistic regression) before reaching for something complex.
- 💡 A model with 99% accuracy on an imbalanced dataset can still be useless — check precision/recall per class.
- 💡 Cross-validation gives a more reliable performance estimate than a single train/test split.
- 💡 Tree-based models (random forest, gradient boosting) are usually the strongest baseline on tabular data.

## Things That Trip People Up

- 🚧 Data leakage: information from the test set (or the future) sneaking into training.
- 🚧 Evaluating only on training data and being surprised by poor real-world performance.
- 🚧 Choosing accuracy as the only metric on an imbalanced classification problem.

## Where You'll Actually Use This

- Credit risk / churn prediction from tabular customer data
- Spam/fraud classification
- Customer segmentation via clustering
- Demand forecasting with regression

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
