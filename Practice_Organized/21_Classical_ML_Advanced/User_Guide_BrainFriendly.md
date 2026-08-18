# Classical Machine Learning — Advanced — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

Beyond the linear/tree baselines in section 16: kernel methods (SVM), probabilistic classifiers (Naive Bayes), boosting (the strongest tabular-data technique in practice), dimensionality reduction, systematic hyperparameter tuning, and classical time-series forecasting.

## What You're About to Learn (and why it matters)

- Support Vector Machines: maximum-margin classification and the kernel trick
- Naive Bayes: a fast, surprisingly strong probabilistic baseline (esp. for text)
- Gradient boosting (GradientBoostingClassifier / XGBoost-style): sequentially correcting errors
- PCA for dimensionality reduction and visualization
- Systematic hyperparameter tuning with GridSearchCV / RandomizedSearchCV
- Classical time-series forecasting (moving averages, ARIMA) vs. the RNN approach from section 17

## Before You Start — Quick Mindset Tips

- 💡 Naive Bayes is a great, very fast first baseline for text classification despite its 'naive' independence assumption.
- 💡 Gradient boosting usually beats random forest on tabular data but is more sensitive to hyperparameters and overfitting.
- 💡 Always scale features before SVM — it's distance-based and sensitive to feature scale, like KNN.
- 💡 Use GridSearchCV/RandomizedSearchCV with cross-validation, not manual trial-and-error tuning on the test set.

## Things That Trip People Up

- 🚧 Tuning hyperparameters against the test set (this is leakage — use a validation set or cross-validation).
- 🚧 Using PCA components as if they were still interpretable original features.
- 🚧 Applying ARIMA to non-stationary data without differencing first.

## Where You'll Actually Use This

- Text classification (spam, sentiment) with Naive Bayes
- High-accuracy tabular prediction competitions/production systems with gradient boosting
- Visualizing high-dimensional customer/product data in 2D with PCA
- Demand/sales forecasting with classical time-series models

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
