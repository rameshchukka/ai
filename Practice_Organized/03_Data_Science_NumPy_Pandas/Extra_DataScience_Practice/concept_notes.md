# NumPy — Concept Notes

NumPy is the reason Python is fast enough for data science. Pure Python loops
over numbers are slow; NumPy replaces them with C-speed operations on arrays.
Every other data/ML library (pandas, sklearn, matplotlib) stores data as NumPy
arrays underneath — understanding NumPy means understanding *all* of them.

## 1. The ndarray — the only thing that matters
A NumPy `ndarray` is a fixed-size, typed, multi-dimensional grid of numbers
stored as one contiguous block of memory. Contrast with a Python list, which
is an array of *pointers* to objects scattered all over memory — that's why
NumPy is orders of magnitude faster for numerical work.

Key attributes to know on any array `a`:
- `a.shape` — a tuple like `(3,)` (1D, 3 elements), `(4, 5)` (4 rows, 5 cols)
- `a.dtype` — the number type: `float64`, `int32`, `bool`, etc.
- `a.ndim` — number of dimensions: 1, 2, 3...
- `a.size` — total number of elements

## 2. Creating arrays
| Function | What you get |
|---|---|
| `np.array([1, 2, 3])` | From a Python list |
| `np.zeros((3, 4))` | All zeros, shape (3,4) |
| `np.ones((2, 5))` | All ones |
| `np.arange(0, 10, 2)` | Like Python range: [0,2,4,6,8] |
| `np.linspace(0, 1, 5)` | 5 evenly-spaced points from 0 to 1 |
| `np.random.randn(3, 3)` | Random normals, shape (3,3) |
| `np.random.randint(0, 10, (3,3))` | Random ints 0-9, shape (3,3) |

## 3. Indexing and slicing
Works like Python lists, but extended to multiple dimensions:
- `a[2]` — 3rd element (1D) or 3rd row (2D)
- `a[1, 3]` — row 1, col 3 of a 2D array
- `a[0:3]` — rows 0, 1, 2
- `a[:, 2]` — ALL rows, column 2 (this is the critical 2D pattern)
- `a[a > 5]` — **boolean indexing**: all elements > 5

## 4. Vectorized operations — the whole point
Operations on arrays happen *element-wise* automatically, without any loop:
```
a = np.array([1, 2, 3])
a * 2        → [2, 4, 6]        (multiply every element)
a + a        → [2, 4, 6]        (add element-wise)
a ** 2       → [1, 4, 9]        (square every element)
np.sqrt(a)   → [1.0, 1.41, 1.73]
```
This replaces `for` loops — always look for a vectorized version before writing a loop over array elements.

## 5. Aggregations
```
a.sum()       total
a.mean()      average
a.std()       standard deviation
a.min() / a.max()
a.argmin() / a.argmax()   index of min/max
```
For 2D arrays: `axis=0` means "collapse rows, result is one value per column";
`axis=1` means "collapse columns, result is one value per row." This trips
everyone up — the worksheet has a visual exercise for this specifically.

## 6. Reshaping
- `a.reshape(4, 3)` — same data, different shape (must have same total elements)
- `a.flatten()` — always gives a 1D copy
- `a.T` — transpose (rows become columns)

## 7. Broadcasting
When two arrays have *different* shapes, NumPy stretches the smaller one along
size-1 dimensions to make them compatible, instead of erroring:
```
a: shape (3, 4)
b: shape (   4)   ← b gets "broadcast" to (3, 4) by repeating across rows
a + b              works, no explicit loop needed
```
Broadcasting is powerful but the mental model takes practice — the worksheet
has a concrete exercise that shows exactly when it works and when it fails.

## 8. Linear algebra (used everywhere in ML)
```
np.dot(a, b)         dot product / matrix multiply
np.linalg.norm(a)    vector magnitude (length)
a / np.linalg.norm(a)   normalize a vector to unit length
np.linalg.eig(a)     eigenvalues and eigenvectors
```
The cosine similarity calculation used throughout the ChromaDB lab is just
`np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))` — after this module
that formula will make obvious sense rather than looking like magic.

## Teaser problem
> You have a 2D array of shape (55, 1024) — 55 embedding vectors, each with
> 1024 dimensions. You want to normalize every row to unit length (divide each
> row by its own magnitude). You try `a / a.norm()` and get an error. Why,
> and what's the correct one-liner?

**Solution:** `np.linalg.norm(a)` with no arguments gives a *single scalar*
(the norm of the whole flattened array) — you need per-row norms, and then
broadcasting to divide each row. Correct: `a / np.linalg.norm(a, axis=1, keepdims=True)`.
`axis=1` computes one norm per row, `keepdims=True` keeps the shape as `(55, 1)`
instead of `(55,)` so broadcasting against `(55, 1024)` works correctly. See
worksheet section 8 for this built up step by step.
