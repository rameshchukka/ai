# 🎓 NumPy & Pandas — Zero to Master Guided Lab

A complete, self-contained course that takes a total beginner to a confident, job-ready
level in NumPy and Pandas. Everything you need is inside the notebooks — theory, worked
examples, exercises, solutions, and real datasets.

## What's inside

| File | What it is |
|---|---|
| `NumPy_Zero_to_Master.ipynb` | 13-chapter guided lab: arrays → indexing → masking → vectorization → broadcasting → aggregations → reshaping → linear algebra → simulation → capstone |
| `Pandas_Zero_to_Master.ipynb` | 13-chapter guided lab: Series/DataFrame → loading → selection → filtering → missing data → cleaning → new columns → sorting → **groupby** → merging → datetime → pivots → capstone |
| `NumPy_Additional_Topics.ipynb` | Gap-fill companion: empty arrays, file I/O (.npy/.csv), random shuffle, 1D transpose edge case, partial sort, split, comparisons, searchsorted, bincount, `numpy.char` string ops |
| `Pandas_Additional_Topics.ipynb` | Gap-fill companion: reading JSON/Excel/GitHub URLs, MultiIndex creation & selection (`.xs`), stack/unstack, `pd.concat`, deleting columns |
| `Zero_to_Master_Guide.html` | Interactive companion guide: how to study, the learning roadmap, and a chapter map |
| `datasets/` | Real, messy datasets the labs use (see below) |

**Full topic coverage.** Between the two main notebooks and their Additional Topics companions,
every core NumPy and Pandas topic is covered: array creation (incl. empty arrays), ndarray
basics, linspace, file I/O (binary `.npy` and text `.csv`), reshape, random sampling & shuffling,
broadcasting, all three indexing styles (basic/integer/boolean), transpose (incl. the 1D
edge case), full & partial sort, concatenate/stack/split, scalar & elementwise comparison,
max-finding & searching (`where` + `searchsorted`), unique values & `bincount`, math functions,
linear algebra, and `numpy.char` string operations — plus, for Pandas: DataFrame fundamentals,
`.loc`/`.iloc`, reading from CSV/JSON/Excel/GitHub URLs, common data-issue cleanup, MultiIndex
creation & selection, reshaping/pivoting (`pivot_table`, `stack`/`unstack`), adding/modifying/
**deleting** columns, `merge` + `concat`, and data transformation (`apply`/`map`).

## Datasets (in `datasets/`)

- **`retail_sales.csv`** (1,010 rows) — the main Pandas teaching dataset. Deliberately messy:
  missing values, duplicate rows, inconsistent text casing — just like real data.
- **`weather_2023.csv`** (365 rows) — daily weather for the datetime / time-series chapter.
- **`customers.csv`** (100 rows) — customer lookup table for the merge/join chapter.
- **`student_scores.csv`** (30×5) — clean numeric grid for the NumPy capstone.

## How to use it

1. **Start with NumPy** (`NumPy_Zero_to_Master.ipynb`), top to bottom. Pandas is built on
   NumPy, so this comes first.
2. Then do **Pandas** (`Pandas_Zero_to_Master.ipynb`).
3. In each chapter: read the 📖 theory → run the 🔬 worked examples → attempt the ✏️ *Your
   Turn* exercise **before** opening the ✅ solution.
4. Finish each notebook's 🏆 **capstone project** — a realistic end-to-end task.

## The teaching format in every chapter

- 📖 **Theory** — the concept in plain language, with a comparison table where useful
- 🧠 **Mental model** — the intuition to hold in your head
- 🔬 **Worked examples** — runnable code you execute and read
- ⚡ **Pro tips** and ⚠️ **common traps** — the things that actually trip people up
- ✏️ **Your Turn** — an exercise to do yourself
- ✅ **Solution** — revealed right after, so you can self-check

## Requirements

```
pip install numpy pandas
```

That's it. Everything runs offline with the bundled datasets.

## After this lab

You'll be ready for the rest of Section 03 (the Module1–4 notebooks and the
`Real_World_Exercises`), and well-prepared for PyTorch (Section 04) and the ML sections,
which all build on NumPy/Pandas fluency.
