# Classical Machine Learning — Advanced — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

Beyond the linear/tree baselines in section 16: kernel methods (SVM), probabilistic classifiers (Naive Bayes), boosting (the strongest tabular-data technique in practice), dimensionality reduction, systematic hyperparameter tuning, and classical time-series forecasting.

## What You Will Learn

- Support Vector Machines: maximum-margin classification and the kernel trick
- Naive Bayes: a fast, surprisingly strong probabilistic baseline (esp. for text)
- Gradient boosting (GradientBoostingClassifier / XGBoost-style): sequentially correcting errors
- PCA for dimensionality reduction and visualization
- Systematic hyperparameter tuning with GridSearchCV / RandomizedSearchCV
- Classical time-series forecasting (moving averages, ARIMA) vs. the RNN approach from section 17

## Important Pointers / Tips

- **Tip:** Naive Bayes is a great, very fast first baseline for text classification despite its 'naive' independence assumption.
- **Tip:** Gradient boosting usually beats random forest on tabular data but is more sensitive to hyperparameters and overfitting.
- **Tip:** Always scale features before SVM — it's distance-based and sensitive to feature scale, like KNN.
- **Tip:** Use GridSearchCV/RandomizedSearchCV with cross-validation, not manual trial-and-error tuning on the test set.
- **Tip:** For time series, always check stationarity before fitting an ARIMA model; differencing often fixes non-stationary data.

## Common Pitfalls

- ⚠️ Tuning hyperparameters against the test set (this is leakage — use a validation set or cross-validation).
- ⚠️ Using PCA components as if they were still interpretable original features.
- ⚠️ Applying ARIMA to non-stationary data without differencing first.

## Real-World Use Cases

- Text classification (spam, sentiment) with Naive Bayes
- High-accuracy tabular prediction competitions/production systems with gradient boosting
- Visualizing high-dimensional customer/product data in 2D with PCA
- Demand/sales forecasting with classical time-series models

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
