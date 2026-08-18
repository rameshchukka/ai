# Scikit-Learn (sklearn) — Concept Notes

sklearn is Python's standard library for machine learning. The ChromaDB lab
uses three sklearn features: PCA (dimensionality reduction for visualization),
KMeans (unsupervised clustering), and TSNE (another visualization method).
This module covers those three plus the broader sklearn patterns — because
understanding the full picture makes those three make more sense.

## 1. The universal sklearn API — learn this once, applies to everything
Every sklearn model, transformer, and estimator follows the same pattern:

```
from sklearn.something import SomeClass

model = SomeClass(param1=..., param2=...)   # 1. create, set hyperparameters
model.fit(X)                                # 2. learn from data
X_transformed = model.transform(X)         # 3. apply (for transformers)
predictions = model.predict(X)             # 4. predict (for classifiers/regressors)
```

Or combined steps 2+3: `model.fit_transform(X)` — this is what the ChromaDB
lab's PCA cells use. Learn this pattern once and you can use any sklearn class.

## 2. Data shape convention
sklearn expects:
- `X`: shape `(n_samples, n_features)` — rows are observations, columns are features
- `y`: shape `(n_samples,)` — one label per observation (for supervised learning)

For your embeddings: `(55, 1024)` means 55 documents, each described by
1024 features. sklearn's PCA, KMeans, TSNE all take this exact shape directly.

## 3. PCA — Dimensionality Reduction
Finds the directions in high-dimensional space that capture the most variance,
projects onto the top N of them. Think of it as "squash 1024 dimensions down
to 2, losing as little information as possible."

```python
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
coords = pca.fit_transform(X)   # X: (55, 1024) → coords: (55, 2)
```

`pca.explained_variance_ratio_` tells you what % of total variance each
component captures — e.g. `[0.35, 0.18]` means component 1 explains 35%
of the variance, component 2 explains 18%, together 53%. The rest is lost.

**When to use PCA:** visualization (reduce to 2 or 3D), speeding up downstream
models, removing noise in highly correlated features.

## 4. KMeans — Unsupervised Clustering
Groups data points into K clusters by minimizing the distance between points
and their assigned cluster center. "Unsupervised" means it finds structure
without needing labels — it discovers groups on its own.

```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=8, random_state=42, n_init=10)
km.fit(X)
labels = km.labels_    # shape (55,) — one cluster id (0-7) per document
centers = km.cluster_centers_  # shape (8, 1024) — the center of each cluster
```

**Choosing K:** the "elbow method" plots inertia (total within-cluster variance)
vs K — you pick the K where adding more clusters stops giving much benefit.
The worksheet shows this. For your 8-topic practice dataset, K=8 should give
good cluster separation.

## 5. t-SNE — Non-linear visualization
Like PCA, reduces to 2D for visualization, but preserves *local neighborhood*
structure (nearby points stay nearby) rather than global variance. Often shows
tighter, more separated clusters visually than PCA, but is slower and
non-deterministic (set `random_state` for reproducibility).

```python
from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, perplexity=10, random_state=42)
coords = tsne.fit_transform(X)   # X: (55, 1024) → coords: (55, 2)
```

`perplexity` controls how much each point looks at local vs global structure.
Typical values: 5-50. For 55 points, use a small value like 10-15.

**Key limitation:** t-SNE has no `transform()` (only `fit_transform()`) —
you can't transform new points into an existing t-SNE embedding. PCA can.
For the ChromaDB lab's live visualization, that's why PCA is the default.

## 6. Supervised learning overview (beyond the ChromaDB lab)
| Model | Task | Key parameter |
|---|---|---|
| `LinearRegression` | Predict a number | — |
| `LogisticRegression` | Classify | `C` (regularization) |
| `RandomForestClassifier` | Classify | `n_estimators`, `max_depth` |
| `SVC` | Classify | `kernel`, `C` |
| `train_test_split` | Split data | `test_size=0.2` |
| `cross_val_score` | Evaluate | `cv=5` |

## 7. Evaluation metrics
```python
from sklearn.metrics import accuracy_score, confusion_matrix, silhouette_score

accuracy_score(y_true, y_pred)      # for classifiers
confusion_matrix(y_true, y_pred)    # table of TP/FP/TN/FN
silhouette_score(X, labels)         # for clustering: how well-separated are clusters?
                                     # range: -1 (bad) to 1 (perfect)
```

`silhouette_score` is directly useful for the ChromaDB lab — it gives you a
number for "how well do these KMeans clusters actually separate the data,"
which is more reliable than eyeballing the scatter plot.

## Teaser problem
> You run KMeans with k=3 on your 55-document embedding dataset. The silhouette
> score is 0.12 (nearly 0, meaning clusters overlap badly). You try k=8 and get
> 0.41 (much better). But you originally chose k=3 because you saw 3 "blob"
> clusters in your PCA scatter plot. Why did k=3 feel right visually but k=8
> score much better numerically?

**Solution:** PCA only shows 2 of 1024 dimensions — the 2 most *globally*
variant, not necessarily the most *discriminative* ones. Three clusters that
look well-separated in 2D PCA can be internally mixed in the remaining 1022
dimensions, which KMeans (working in full 1024D) knows about and PCA is not
showing you. This is why the workshop uses *both* visualization (to build
intuition) and silhouette score (to actually measure quality) — neither alone
is sufficient. See worksheet section 4 for this exact demonstration.
