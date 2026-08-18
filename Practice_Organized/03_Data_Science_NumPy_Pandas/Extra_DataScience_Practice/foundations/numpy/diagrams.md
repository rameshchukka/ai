# NumPy — Diagrams

## 1. Array shapes visualized

```
1D array — shape (5,)
┌───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │
└───┴───┴───┴───┴───┘

2D array — shape (3, 4)   "3 rows, 4 columns"
        col0  col1  col2  col3
row0  ┌────┬────┬────┬────┐
      │  1 │  2 │  3 │  4 │
row1  ├────┼────┼────┼────┤
      │  5 │  6 │  7 │  8 │
row2  ├────┼────┼────┼────┤
      │  9 │ 10 │ 11 │ 12 │
      └────┴────┴────┴────┘

a[1, 2] → 7           (row 1, col 2)
a[:, 2] → [3, 7, 11]  (all rows, col 2)
a[0, :] → [1, 2, 3, 4] (row 0, all cols)
```

## 2. axis=0 vs axis=1, visualized

```
a = shape (3, 4)

axis=0: "collapse ROWS → one value per COLUMN"
        col0  col1  col2  col3
row0  │  1 │  2 │  3 │  4 │
row1  │  5 │  6 │  7 │  8 │   sum(axis=0) → [15, 18, 21, 24]
row2  │  9 │ 10 │ 11 │ 12 │
         ↓    ↓    ↓    ↓
        15   18   21   24     shape: (4,)

axis=1: "collapse COLUMNS → one value per ROW"
row0  │  1 │  2 │  3 │  4 │ →  10
row1  │  5 │  6 │  7 │  8 │ →  26   sum(axis=1) → [10, 26, 42]
row2  │  9 │ 10 │ 11 │ 12 │ →  42
                                      shape: (3,)
```

## 3. Broadcasting rules

```
WORKS:
a: (3, 4)    b: (4,)   →  b treated as (1, 4), stretched to (3, 4)  ✓
a: (3, 4)    b: (3, 1) →  b stretched to (3, 4)                     ✓
a: (3, 1)    b: (1, 4) →  both stretched to (3, 4)                  ✓

FAILS:
a: (3, 4)    b: (3,)   →  shapes don't align from the right          ✗
                           (3,4) vs (3,) → (3,4) vs (1,3)
                           4 ≠ 3 and neither is 1 → error

RULE: align shapes from the RIGHT.
Dimensions must be either equal OR one of them must be 1.
```

## 4. Cosine similarity, built from NumPy primitives

```
Two vectors:  a = [0.2, 0.5, 0.1]
              b = [0.3, 0.4, 0.2]

Step 1: dot product    np.dot(a, b) = 0.2*0.3 + 0.5*0.4 + 0.1*0.2 = 0.28
Step 2: magnitudes     np.linalg.norm(a) = √(0.04+0.25+0.01) = 0.548
                       np.linalg.norm(b) = √(0.09+0.16+0.04) = 0.539
Step 3: similarity     0.28 / (0.548 * 0.539) = 0.948

Range: -1 (opposite) to 0 (unrelated) to 1 (identical direction)
This is exactly what Chroma does when you set distance="cosine"
```
