# Practice Topics

Your first-contact dataset — 8 clean topics with deliberately planted near-duplicates, bridge docs, and outliers so the embedding space has obvious, learnable structure.

**Dataset:** `dataset/practice_dataset.xlsx` — 55 rows
**Metadata fields:** `topic (8 subjects)`, `type (core / near_duplicate / bridge / outlier)`

## What this dataset teaches
How a healthy embedding space looks: same-topic docs cluster, near-duplicates sit on top of each other, bridges float between clusters, outliers sit alone. The baseline 'good' you compare messier data against.

---

## 1. Ingestion
1. Load `practice_dataset.xlsx` (columns: id, text, topic, type, notes).
2. Embed the `text` column; put `topic` and `type` into metadata.
3. Ingest all 55 rows into a collection named `practice_topics`.

Run `ingestion_examination.ipynb` in this folder — it does the ingestion above and
then walks the examination below. It defaults to an offline mock embedder so it runs
immediately; set `USE_MOCK = False` (or swap in `InHouseEmbeddings()`) for the real
in-house Jina model, which sharpens retrieval quality.

To regenerate or tweak the dataset itself, run `dataset/build_dataset.py`.

## 2. Examination in Chroma Studio
Point Chroma Studio's sidebar at this collection's folder, then:

- **Visualize → color by `topic`** — You should see 8 distinct clusters — the baseline 'the embedding space makes sense' check.
- **Visualize → color by `type`** — `near_duplicate` points sit on top of their originals; `bridge` points float between two clusters; `outlier` points sit alone.
- **Search → 'how does high heat affect vegetables'** — The cooking near-duplicate pair both return with nearly identical distances — near-duplication made visible.
- **Cluster → k=8** — Auto-discovered clusters should mostly line up with the 8 topics; where they don't is where bridges/outliers live.

The notebook computes the same things in code (so you understand what each view
shows); Studio is the interactive version of the same checks.

## 3. Enrichment — decisions this dataset lets you practice
- Add a `difficulty` or `source` metadata field via Edit/Update (metadata-only, no re-embed) and re-color the plot by it.
- Deliberately mislabel one row's `topic`, then use the cluster view to catch that its neighbors disagree — practice the detection before doing it on messy data.

Enrichment via metadata (Edit/Update tab) is instant — a metadata-only change does
NOT re-embed. Only changing a document's **text** triggers re-embedding.

---

*Part of the Chroma Studio Datasets collection. See `../_guide/` for the full feature
guide and `../README.md` for the learning order across all five datasets.*
