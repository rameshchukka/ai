# Support KB with Planted Flaws

A support knowledge base with six deliberately planted flaws — the analyze→decide→act capstone. This is where you practice diagnosing a messy corpus.

**Dataset:** `dataset/support_kb.csv` — 21 rows
**Metadata fields:** `category`, `product`, `flaw (hidden answer key)`

## What this dataset teaches
The full decision loop: spot a problem in a Studio view, decide the fix (enrich / dedupe / fix metadata / re-chunk / add filter), apply it, recheck. The `flaw` column is a hidden answer key to check your findings.

---

## 1. Ingestion
1. Load `support_kb.csv` (columns: id, text, category, product, flaw).
2. Embed `text`; put `category` and `product` into metadata. **Do NOT embed or filter on `flaw`** — it's the answer key, kept only to verify your diagnoses.
3. Ingest into a collection named `support_flaws`.

Run `ingestion_examination.ipynb` in this folder — it does the ingestion above and
then walks the examination below. It defaults to an offline mock embedder so it runs
immediately; set `USE_MOCK = False` (or swap in `InHouseEmbeddings()`) for the real
in-house Jina model, which sharpens retrieval quality.

To regenerate or tweak the dataset itself, run `dataset/build_dataset.py`.

## 2. Examination in Chroma Studio
Point Chroma Studio's sidebar at this collection's folder, then:

- **Visualize → color by `category`** — Find the lone `compliance` point — thin coverage.
- **Visualize → stacked points** — The refund docs cluster tightly — near-duplicates.
- **Cluster vs `category` cross-tab** — Where KMeans disagrees with your labels = metadata you can't trust.
- **Browse → filter blank `category`** — Missing-metadata docs, invisible to any category-filtered query.
- **Search → a muddy result** — The overlong doc cramming 3 topics returns weakly for everything — a re-chunk signal.

The notebook computes the same things in code (so you understand what each view
shows); Studio is the interactive version of the same checks.

## 3. Enrichment — decisions this dataset lets you practice
- Dedupe: delete redundant refund docs, keeping the most complete one.
- Fix the mislabeled doc's `category` (metadata-only update, instant).
- Re-chunk the overlong mixed doc into focused docs (delete + add 3).
- Add an `intent` field to disambiguate the cancel-subscription vs cancel-order collision.
- Backfill blank `category` values, then review the inferred labels.

Enrichment via metadata (Edit/Update tab) is instant — a metadata-only change does
NOT re-embed. Only changing a document's **text** triggers re-embedding.

---

*Part of the Chroma Studio Datasets collection. See `../_guide/` for the full feature
guide and `../README.md` for the learning order across all five datasets.*
