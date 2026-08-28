# Chroma Practice Lab

A self-contained sandbox to build two skills together: (1) intuition for how
embeddings/clustering/retrieval actually behave, and (2) operational comfort
ingesting data into Chroma via its real REST API — both transferable straight to
your actual project's data ingestion and retrieval work.

## Read in this order

1. **`DataSetReadme.md`** — what's in `dataset/practice_dataset.xlsx` and why it's
   designed the way it is (8 disjoint clusters, near-duplicates, bridge docs, outliers).
2. **`ConceptualIntuition.ipynb`** — confirm the dataset behaves as designed,
   numerically, with no Chroma server needed yet.
3. **`IngestionProcess.md`** — the 4-step ingestion pipeline explained, pointing to:
   - `ingestion/manual_curl_examples.sh` — do this by hand first, a few rows
   - `ingestion/bulk_ingest_from_excel.ipynb` — then load everything, batched
4. **`ChromaNavigatorGuide.md`** — what to look for in each tab of the Navigator,
   specific to this dataset's known structure.
5. **`ingestion/jmeter_load_test.jmx`** — once ingestion is verified correct, load-test
   the embedding + Chroma endpoints separately (ingestion load vs. query load).

## Folder structure
```
chroma_practice_lab/
├── README.md                          (this file)
├── DataSetReadme.md
├── ChromaNavigatorGuide.md
├── IngestionProcess.md
├── ConceptualIntuition.ipynb
├── dataset/
│   ├── practice_dataset.xlsx          (the 55-row dataset)
│   └── build_dataset.py               (regenerate/modify the dataset)
└── ingestion/
    ├── manual_curl_examples.sh
    ├── bulk_ingest_from_excel.ipynb
    ├── jmeter_load_test.jmx
    ├── jmeter_ingest_rows.csv
    └── jmeter_query_vector.csv        (placeholder vectors - regenerate with real ones)
```

## Before you start, fill in 2 things everywhere they appear
- Your Chroma server's **host/port** (default placeholders: `localhost:8000`)
- Your collection's **UUID**, resolved once via the v2 API's collection-list call

The third thing from earlier versions of this lab — the embedding endpoint's
request/response shape — is no longer a guess. It's now hardcoded correctly
throughout (`manual_curl_examples.sh`, `bulk_ingest_from_excel.ipynb`,
`ConceptualIntuition.ipynb`) using the real values from your `inhouse_llm.py`
(`API_BASE_JINA`, `API_KEY`). You'll still need to paste your real `API_KEY`
value into `manual_curl_examples.sh` directly (it's read from your environment
automatically in the notebooks, via the corrected `inhouse_wrappers.py`).

## A note on realism vs. cleanliness
This dataset is deliberately clean and small so the *behavior* is easy to see. Once
this all clicks, the next worthwhile step is intentionally messier data: more topic
overlap, real near-duplicates from your own corpus, ambiguous documents that don't
fit your taxonomy. That's where the debugging instincts you're building here actually
get tested.
