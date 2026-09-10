# Week 4 Quiz — Clustering
**Total points: 15** (5 questions × 3 points)

---

### Q1. Which statement is **NOT TRUE** about k-means clustering?
- ( ) k-means divides the data into non-overlapping clusters without any cluster-internal structure.
- ( ) The objective of k-means is to form clusters in such a way that similar samples go into a cluster, and dissimilar samples fall into different clusters.
- (●) **As k-means is an iterative algorithm, it guarantees that it will always converge to the global optimum.**

**Why:** This is the false statement. k-means is sensitive to its random initial centroid
placement and can converge to a **local optimum**, not necessarily the global one — this is
exactly why in practice you run k-means multiple times with different initializations
(`n_init` in scikit-learn) and keep the best result.

---

### Q2. Which of the following are characteristics of DBSCAN? *(select all that apply)*
- (✅) **DBSCAN can find arbitrarily shaped clusters.**
- (✅) **DBSCAN can find a cluster completely surrounded by a different cluster.**
- (✅) **DBSCAN has a notion of noise, and is robust to outliers.**
- (✅) **DBSCAN does not require one to specify the number of clusters such as k in k-means.**

**Why:** All four are genuine, well-known strengths of DBSCAN (density-based clustering) over
k-means: it doesn't assume spherical/convex cluster shapes, can find nested/surrounded
clusters, explicitly labels noise/outlier points rather than forcing them into a cluster, and
determines the number of clusters automatically from the data's density structure.

---

### Q3. Which of the following is an application of clustering?
- ( ) Customer churn prediction
- ( ) Price estimation
- (●) **Customer segmentation**
- ( ) Sales prediction

**Why:** Customer segmentation — grouping customers by similarity with no predefined labels —
is the classic clustering (unsupervised) use case. Churn prediction, price estimation, and
sales prediction are all **supervised** tasks (you have a known outcome to predict).

---

### Q4. Which approach can be used to calculate dissimilarity of objects in clustering?
- ( ) Minkowski distance
- ( ) Euclidian distance
- ( ) Cosine similarity
- (●) **All of the above**

**Why:** All three are valid distance/dissimilarity metrics that can be used in clustering,
depending on the nature of the data — Euclidean for typical continuous features, Minkowski as
a generalization of Euclidean/Manhattan distance, and cosine similarity especially for
high-dimensional or text/vector data where the angle between vectors matters more than raw
magnitude.

---

### Q5. How is a center point (centroid) picked for each cluster in k-means? *(select all that apply)*
- (✅) **We can randomly choose some observations out of the data set and use these observations as the initial means.**
- (✅) **We can create some random points as centroids of the clusters.**
- ( ) We can select it through correlation analysis.

**Why:** k-means initializes centroids either by randomly picking actual data points, or by
generating random points in the feature space — both are standard initialization strategies.
"Correlation analysis" isn't part of how k-means initializes centroids at all, correctly
excluded.
