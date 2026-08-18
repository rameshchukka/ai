# 📊 Python for Data Science Course — Advanced Idioms

Part of an uploaded external course (`python_for_datascience-master`, Pragmatic AI Labs). This
folder has the **more advanced Python idiom lessons** — functional programming style, lazy
evaluation, and pattern matching are intermediate/advanced topics that fit better alongside
this section's other advanced exercises than with basics-level material.

## Lessons here

| File | Topic |
|---|---|
| `Lesson10_..._Functional_Programming.ipynb` | Functional programming (map/filter/reduce, etc.) |
| `Lesson11_..._Lazy_Evaluation.ipynb` | Lazy evaluation (generators, iterators) |
| `Lesson12_..._Pattern_Matching.ipynb` | Pattern matching |
| `Lesson14_..._I_O.ipynb` | I/O (files, CSV, Google Sheets) |

## What was found and fixed

Two cells are genuinely tied to Google Colab's environment and will raise
`ModuleNotFoundError` anywhere else — flagged inline with a portable alternative:

| Notebook | Issue | Fix noted inline |
|---|---|---|
| Lazy Evaluation | `google.colab.files.upload()` | Load the file by path directly outside Colab |
| I/O | `google.colab.auth.authenticate_user()` for Google Sheets | Use `gspread.service_account(...)` outside Colab |

## The rest of this course, by topic

| Topic | Where |
|---|---|
| Basics, Strings, Data Structures, Data Conversion, Execution Control, Functions | `../../01_Python_Basics/External_Python_for_DataScience_Course/` |
| Sorting | `../../19_Algorithms_and_Data_Structures/External_Python_for_DataScience_Course/` |
| Case Studies | `../../03_Data_Science_NumPy_Pandas/External_Python_for_DataScience_Course/` |
