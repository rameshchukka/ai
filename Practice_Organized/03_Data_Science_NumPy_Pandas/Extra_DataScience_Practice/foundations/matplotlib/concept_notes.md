# Matplotlib — Concept Notes

Matplotlib is Python's core plotting library. Everything you saw in the
ChromaDB lab (scatter plots, PCA visualizations, cluster coloring) came
from matplotlib. The key mental model: you're building a figure like a
canvas — you add one or more axes (plot areas) to it, then draw onto each axis.

## 1. Two interfaces — know which one you're using
| Interface | Style | When to use |
|---|---|---|
| `plt.plot(...)` / `plt.show()` | Stateful, implicit | Quick one-off plots in a notebook |
| `fig, ax = plt.subplots()` / `ax.plot(...)` | Object-oriented, explicit | Multiple subplots, customization, code you'll reuse |

The ChromaDB lab and sklearn exercises use the object-oriented style throughout
since it scales to multiple side-by-side plots cleanly.

## 2. The most-used plot types
| Function | What it shows | When to reach for it |
|---|---|---|
| `ax.plot(x, y)` | Line chart | Trends over time or a continuous variable |
| `ax.scatter(x, y)` | Scatter plot | Relationship between two variables, or 2D data points (embeddings!) |
| `ax.bar(labels, heights)` | Bar chart | Comparing categories |
| `ax.hist(data, bins=20)` | Histogram | Distribution of one variable |
| `ax.boxplot(data)` | Box plot | Distribution + outliers, good for comparing groups |
| `ax.imshow(matrix)` | Heatmap/image | Confusion matrices, correlation matrices |

## 3. Anatomy of a plot — things you'll customize
```
fig.suptitle("Overall figure title")
ax.set_title("This subplot's title")
ax.set_xlabel("X axis label")
ax.set_ylabel("Y axis label")
ax.legend()                  — shows legend (needs label= on each plot call)
ax.set_xlim(0, 10)           — fix the x axis range
ax.set_ylim(-1, 1)           — fix the y axis range
ax.grid(True)                — add gridlines
fig.tight_layout()           — prevent labels overlapping between subplots
```

## 4. Coloring and markers
- `color="red"` or `color="#FF5733"` (hex) or `color=(0.2, 0.8, 0.3)` (RGB)
- `alpha=0.6` — transparency (0=invisible, 1=solid), useful when dots overlap
- `s=50` — dot size in scatter plots
- `c=array` — color each point differently, using a numeric array + colormap
- `cmap="tab10"` — a colormap; `"tab10"` gives 10 distinct colors, great for labeled clusters

## 5. Subplots — side by side comparisons
```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# axes is now an array: axes[0] is left plot, axes[1] is right plot
axes[0].scatter(...)
axes[1].scatter(...)
plt.show()
```
This is exactly how the ChromaDB lab's "PCA vs t-SNE comparison" cell works.

## 6. Saving a figure
```python
fig.savefig("my_plot.png", dpi=150, bbox_inches="tight")
```
`bbox_inches="tight"` prevents labels being cut off at the edges.

## Teaser problem
> You plot a PCA scatter of 55 embedding vectors. All the dots appear in one
> dense blob, impossible to distinguish by eye. What are 3 different matplotlib
> techniques to make the structure visible?

**Solution:**
1. **Color by label** — `ax.scatter(x, y, c=labels_array, cmap="tab10")` uses
   a different color per label, so clusters separate visually even if spatially
   close.
2. **Alpha transparency** — `alpha=0.6` lets overlapping dots show through
   each other instead of solid blobs hiding density.
3. **Annotate specific points** — `ax.annotate("doc_01", (x[0], y[0]))` labels
   individual points so you can identify specific documents like near-duplicates.
   See worksheet section 6 for all three combined on the practice dataset.
