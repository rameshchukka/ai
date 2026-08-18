# 📈 Google Colab for Data Science & AI Exercises

9 exercise-module notebooks from the uploaded `Google-Colab-for-Data-Science-AI-using-Python-main`
repo, plus the real dataset they use (`AirQualityUCI.csv`) and a small `sample.txt`.

## Contents

`Exercises_Module_1.ipynb` through `Exercises_Module_9.ipynb` — a progressive series of
data-science exercises in Python (pandas/numpy-driven, using the real UCI Air Quality dataset).

## Verification done

- All 9 notebooks: valid JSON
- Scanned for Colab-only code (`google.colab` imports) and hardcoded local file paths

## What was found

No portability issues. Some notebooks (Modules 4, 8, 9) contain leftover cached **display
output** referencing `google.colab` — that's just stale HTML/JS from Colab's interactive
dataframe-viewer widget, saved the last time the notebook ran in Colab. It's cosmetic only
(not code you run) and gets replaced automatically the next time you execute those cells in
any environment — no fix needed.

No hardcoded absolute paths were found; `AirQualityUCI.csv` is referenced by relative path and
is included in this folder.
