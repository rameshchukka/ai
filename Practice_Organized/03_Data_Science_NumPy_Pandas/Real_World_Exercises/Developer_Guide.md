# NumPy & Pandas for Real-World Data Work — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

NumPy gives you fast, vectorized arrays; Pandas builds on NumPy to give you labeled, tabular data (like Excel/SQL, but programmable). Together they're the foundation of almost every data and ML pipeline in Python.

## What You Will Learn

- Vectorized array operations and broadcasting (NumPy)
- Loading, inspecting, and cleaning real datasets (read_csv, info, describe, isna)
- Filtering, sorting, and querying DataFrames like a database
- GroupBy + aggregation for business-style reporting
- Merging/joining multiple data sources
- Datetime handling and time-series resampling
- apply/map/vectorized string ops for feature engineering

## Important Pointers / Tips

- **Tip:** Prefer vectorized operations over `for` loops or `.iterrows()` — it's 10-100x faster.
- **Tip:** `df.copy()` before mutating a filtered slice to avoid the SettingWithCopyWarning.
- **Tip:** Always check `df.dtypes` and `df.isna().sum()` right after loading data — most bugs start here.
- **Tip:** `groupby().agg()` with a dict of column->function is the most flexible reporting pattern.
- **Tip:** Use `axis=0` for 'down the rows / per column' and `axis=1` for 'across the columns / per row' — this trips up everyone at first.
- **Tip:** `merge(how=...)` mirrors SQL joins: inner, left, right, outer — pick deliberately, don't default to inner.

## Common Pitfalls

- ⚠️ Chained indexing like `df[df.x>0]['y'] = 1` silently fails to update the original — use `.loc[]`.
- ⚠️ Comparing floats for exact equality after arithmetic; use `np.isclose`.
- ⚠️ Forgetting `parse_dates=` when reading CSVs with date columns — they load as strings.
- ⚠️ Using Python `and`/`or` instead of `&`/`|` on boolean arrays/Series.

## Real-World Use Cases

- Sales/revenue reporting by product, region, and time period
- Cleaning messy survey or log data (missing values, inconsistent types)
- Building features for an ML model from raw transaction data
- Time-series resampling of sensor/IoT data to hourly/daily aggregates

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
