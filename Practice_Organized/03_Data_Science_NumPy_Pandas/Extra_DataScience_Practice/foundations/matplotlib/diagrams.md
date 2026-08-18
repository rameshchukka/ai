# Matplotlib — Diagrams

## 1. Figure and Axes hierarchy

```
Figure  (the whole canvas / window)
  │
  ├── Axes 0  (one plot area — has its own x/y axes, title, labels)
  │     ├── title
  │     ├── x-axis (label, ticks, limits)
  │     ├── y-axis (label, ticks, limits)
  │     └── plotted elements (lines, dots, bars, ...)
  │
  └── Axes 1  (a second plot area, side-by-side or below)
        └── ...

fig, axes = plt.subplots(1, 2)
             ↑                ↑
         one Figure     two Axes objects in a 1×2 grid
```

## 2. The object-oriented call pattern

```
fig, ax = plt.subplots(figsize=(8, 5))
            │
            │  ← creates both Figure AND one Axes in one call
            ↓
ax.scatter(x, y, c=colors, alpha=0.7, s=60, cmap="tab10")
ax.set_title("My Plot")
ax.set_xlabel("PCA dimension 1")
ax.set_ylabel("PCA dimension 2")
ax.legend()
plt.show()
```

## 3. Color-coding cluster scatter (pattern from ChromaDB lab)

```
For each unique label, plot that label's subset separately:
  ↓ gives each group its own legend entry

for label in unique_labels:
    idx = [i for i, l in enumerate(all_labels) if l == label]
    ax.scatter(coords[idx, 0],    ← x coords for this group
               coords[idx, 1],    ← y coords for this group
               label=label,        ← legend text
               alpha=0.7,
               s=60)
ax.legend()

vs. using c= for automatic coloring:

ax.scatter(coords[:, 0], coords[:, 1],
           c=numeric_labels,       ← one number per point
           cmap="tab10",           ← maps numbers to colors
           alpha=0.7)
```

## 4. Common subplot layouts

```
plt.subplots(1, 2)   →  [ax0] [ax1]           side by side

plt.subplots(2, 1)   →  [ax0]                 stacked
                        [ax1]

plt.subplots(2, 3)   →  [ax0][ax1][ax2]       grid
                        [ax3][ax4][ax5]
```
