# Support Docs — Rich Metadata

A small, clean support set with FOUR metadata fields — the dataset for verifying that metadata ingestion and filtering actually work end to end.

**Dataset:** `dataset/support_docs.csv` — 16 rows
**Metadata fields:** `topic`, `type`, `product`, `priority`

## What this dataset teaches
That metadata survives ingestion and every filter type works: summary counts, equality filter, multi-value ($in), and combined ($and). The notebook asserts exact counts so it fails loudly if anything's wrong.

---

## 1. Ingestion
1. Load `support_docs.csv` (columns: id, text, topic, type, product, priority).
2. Embed `text`; put all four of topic/type/product/priority into metadata.
3. Ingest into a collection named `support_metadata`.

Run `ingestion_examination.ipynb` in this folder — it does the ingestion above and
then walks the examination below. It defaults to an offline mock embedder so it runs
immediately; set `USE_MOCK = False` (or swap in `InHouseEmbeddings()`) for the real
in-house Jina model, which sharpens retrieval quality.

To regenerate or tweak the dataset itself, run `dataset/build_dataset.py`.

## 2. Examination in Chroma Studio
Point Chroma Studio's sidebar at this collection's folder, then:

- **Browse → Metadata summary** — Counts per value must match the dataset (topic: 5 values, priority: high/medium/low, etc.).
- **Browse → filter `topic = finance`** — Exactly 4 docs.
- **Browse → filter `priority` in [high, medium]** — Multi-value $in filter.
- **Visualize → color by `product`, filter `priority = high`** — The filtered-plot path.

The notebook computes the same things in code (so you understand what each view
shows); Studio is the interactive version of the same checks.

## 3. Enrichment — decisions this dataset lets you practice
- This dataset is deliberately clean — use it to practice ADDING structure: introduce a new `region` field on a subset, then confirm it appears in the summary and as a filter/color option.
- Combine filters (topic=finance AND priority=high) to confirm $and works before relying on it in real work.

Enrichment via metadata (Edit/Update tab) is instant — a metadata-only change does
NOT re-embed. Only changing a document's **text** triggers re-embedding.

---

*Part of the Chroma Studio Datasets collection. See `../_guide/` for the full feature
guide and `../README.md` for the learning order across all five datasets.*
