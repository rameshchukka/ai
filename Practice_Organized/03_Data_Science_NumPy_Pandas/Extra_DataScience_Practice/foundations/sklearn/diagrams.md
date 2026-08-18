# Scikit-Learn — Diagrams

## 1. Universal sklearn API flow

```
                     (n_samples, n_features)
                              ↓
model = SomeClass(params)
         │
         ↓
model.fit(X)          ← learns from data, modifies model internally
         │
         ├── model.transform(X)   → (n_samples, n_components)  [transformers]
         │                            PCA, TSNE, StandardScaler
         │
         └── model.predict(X)    → (n_samples,)                [estimators]
                                     KMeans, LogisticRegression, etc.

Shortcut for transformers:
model.fit_transform(X)  ≡  model.fit(X); model.transform(X)
```

## 2. PCA: from 1024D to 2D

```
Original data: (55, 1024) — 55 docs, each described by 1024 numbers
       │
       ↓  PCA(n_components=2).fit_transform()
       │
2D coords: (55, 2) — 55 docs, now described by just 2 numbers
       │
       ↓  matplotlib scatter
       │
Scatter plot you can actually look at
       │
       └── color by topic → see if same-topic docs cluster together
           color by type  → see where near-duplicates (red) land
```

## 3. KMeans: how it works (conceptually)

```
Step 1: Randomly place K cluster centers
        ×  ×  ×  ×  ×  ×  ×  ×   (K=3 here)
         C1           C2    C3

Step 2: Assign each point to its nearest center
        points near C1 → cluster 0
        points near C2 → cluster 1
        points near C3 → cluster 2

Step 3: Recalculate center = mean of all assigned points
        C1 moves to the center of cluster 0's points
        C2 moves to center of cluster 1's points  etc.

Step 4: Repeat steps 2+3 until centers stop moving

Result: km.labels_  → [0, 1, 0, 2, 1, 0, ...]  one id per document
```

## 4. Elbow method — choosing K

```
inertia (lower = tighter clusters)
│
│  *
│    *
│      *
│        *
│           *
│               *  *  *  *  *  *
└─────────────────────────────────── k
   1  2  3  4  5  6  7  8  9  10

Pick K at the "elbow" — where adding more clusters stops
giving large drops in inertia. Here: K=4 or K=5.
```

## 5. t-SNE vs PCA, when they disagree

```
PCA (linear, preserves global structure):
 All 55 points compressed into 2 directions of max variance.
 Good at showing broad separation of very different topics.
 May merge topics that are close but distinct in high dimensions.

t-SNE (non-linear, preserves local neighborhoods):
 Each point stays close to its actual nearest neighbors.
 Usually shows tighter, more distinct clusters.
 Slow, non-deterministic, no transform() for new points.

USE BOTH:
 PCA first → quick sanity check, is there ANY structure visible?
 t-SNE if PCA looks like one blob → more powerful lens to find structure
 Silhouette score on full-dim data → actual measure, not visual guess
```
