# IBM AI Engineering Professional Certificate — Inspection & Study Notes

## What's actually in this repo
This repo (a third-party fork/collection, not the full 13-course specialization) contains
material for only **Course 1: Machine Learning with Python**:

| Week | Content | Type |
|---|---|---|
| 1 | Intro to Machine Learning | PDF quiz — no code |
| 2 | Regression | PDF quiz — no code |
| 3 | Classification | PDF quiz — no code |
| 4 | Clustering | PDF quiz — no code |
| 5 | Recommender System | PDF quiz — no code |
| 6 | **Loan Prediction capstone** | **2 notebooks — the only code exercise in this repo** |

Weeks 1–5 are PDF-format quizzes, not notebooks — there's nothing to inspect, complete, or
annotate cell-by-cell for those (a PDF isn't executable code).

## The Week 6 capstone — completeness check
Two notebooks cover the SAME assignment (the classic IBM "best classifier" loan-prediction
capstone — predict whether a loan will be paid off using KNN, Decision Tree, SVM, and
Logistic Regression, then compare all four on Jaccard score, F1 score, and Log Loss):

- **`ML0101EN-Proj-Loan-py-v1.ipynb`** — the blank ASSIGNMENT TEMPLATE. 15 of its 37 code
  cells are empty stubs (exactly the KNN/Decision Tree/SVM/Logistic Regression model-building
  sections, plus loading the official test set) — this is what a learner would fill in.
- **`submission.ipynb`** — a COMPLETE, correct solution to the identical assignment. All 42
  code cells are filled in and the logic is sound (verified by reading every cell).

**Since a complete, correct solution to this exact assignment already exists
(`submission.ipynb`), there was nothing left un-completed** — I annotated that file rather
than separately re-filling the blank template with identical code. If you specifically need
the blanks filled IN THE TEMPLATE FILE ITSELF (e.g. for a Coursera filename requirement), say
so and I'll copy the same solved code into `ML0101EN-Proj-Loan-py-v1.ipynb`'s blank cells.

## What was added to `submission.ipynb`
1. **A 📘 Fundamentals Required banner** at the very top — an extensive (not a bullet-point
   summary) primer covering: the end-to-end ML workflow this notebook follows, why FOUR
   different algorithms are compared at all, the core pandas/NumPy/Matplotlib/Seaborn/
   scikit-learn tools used throughout, and — in real depth — why train/test splitting and
   feature standardization matter.
2. **A 📎 CONCEPT/FUNDAMENTALS note before every one of the 42 non-empty code cells** — each
   a genuine multi-sentence-to-multi-paragraph explanation (not a two-liner), covering both
   WHAT the cell does and the underlying concept: feature engineering and binarization, label
   vs. one-hot encoding and the dummy-variable trap, the X/y convention, why standardize,
   train/test splitting and reproducibility via `random_state`, and — in full depth for each —
   how K-Nearest Neighbors, Decision Trees (entropy/information gain, `max_depth` as an
   overfitting control), Support Vector Machines (max-margin hyperplanes, the kernel trick),
   and Logistic Regression (the sigmoid function, regularization via `C`) each actually work,
   plus the Jaccard score / F1 score / Log Loss evaluation metrics and why only Logistic
   Regression gets a Log Loss (it's the only model here producing real probabilities).

**42/42 code cells covered — full coverage, nothing skipped.**

## Honesty notes
- I verified `submission.ipynb`'s code is standard, correct, well-known IBM course code — not
  just "non-empty," but logically sound end to end (train/test split → tune k → train all
  four models → evaluate all four on the real held-out `loan_test.csv`).
- I did not execute the notebook here (it needs the two CSV files downloaded via the
  commented-out `wget`/`!wget` cells, plus `seaborn` installed) — the concept notes are based
  on reading the code, and the results table already baked into the notebook's own markdown
  (Jaccard/F1/LogLoss per algorithm) is the original author's reported output, not something
  I re-ran.
