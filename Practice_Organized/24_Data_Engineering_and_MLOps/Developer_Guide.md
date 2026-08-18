# Data Engineering & MLOps — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

The plumbing that turns a working notebook into a reliable production system: moving and transforming data reliably (ETL/orchestration), processing at scale, deploying and tracking models, telling a clear visual story with data, and querying efficiently at scale with SQL.

## What You Will Learn

- ETL/ELT pipeline basics: extract, transform, load, and why order matters
- Orchestration concepts (DAGs, scheduling, retries) as used by tools like Airflow/Prefect
- Distributed data processing concepts (what Spark solves that Pandas can't)
- Model deployment & tracking basics (model registry, versioning, experiment tracking)
- Effective data visualization (choosing the right chart, avoiding misleading visuals)
- Advanced SQL: window functions, joins at scale, query optimization/indexing basics

## Important Pointers / Tips

- **Tip:** Design pipelines to be idempotent (safe to re-run) — production pipelines fail and get retried constantly.
- **Tip:** A DAG (directed acyclic graph) models task dependencies explicitly — this is why orchestration tools use DAGs, not simple linear scripts.
- **Tip:** Reach for Spark (or similar) only when data no longer fits in memory on one machine — Pandas is simpler and faster to develop with below that threshold.
- **Tip:** Version your models and datasets together — reproducing 'why did prediction X happen' requires knowing exactly what model + data produced it.
- **Tip:** Window functions (`OVER (PARTITION BY ... ORDER BY ...)`) solve 'running total per group' and 'rank within group' problems that are painful with plain GROUP BY.

## Common Pitfalls

- ⚠️ Silent pipeline failures with no alerting — a broken pipeline that fails quietly is worse than one that fails loudly.
- ⚠️ Scaling to Spark/distributed tools prematurely, before Pandas actually stops being sufficient.
- ⚠️ Choosing a chart type that visually exaggerates or hides the real effect size (e.g., truncated y-axis).
- ⚠️ Missing indexes on frequently-filtered/joined SQL columns, causing full table scans at scale.

## Real-World Use Cases

- Nightly ETL jobs that refresh a reporting dashboard
- Model registries tracking which model version is live in production
- Executive dashboards that need to communicate a clear, honest visual story
- Analytics queries computing running totals, rankings, or cohort retention with SQL window functions

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
