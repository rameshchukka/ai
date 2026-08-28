# Chroma Studio Datasets

Every teaching dataset for Chroma Studio, organized. Each of the five folders is
self-contained and identical in shape:

```
NN_name/
├── dataset/
│   ├── <data file>          the dataset itself (csv or xlsx)
│   └── build_dataset.py     regenerate/tweak it
├── ingestion_examination.ipynb   ingest + examine, runs offline out of the box
└── README.md                ingestion → examination → enrichment for THIS dataset
```

Plus `_guide/chroma_studio_guide.html` — the full feature reference for the Studio app.

## Start here — the learning order

Work through them in number order. Each builds intuition the next one assumes.

| # | Dataset | Rows | Teaches | Metadata to filter on |
|---|---|---|---|---|
| **01** | Practice Topics | 55 | What a *healthy* embedding space looks like | `topic`, `type` |
| **02** | Support KB (flawed) | 21 | Diagnosing a *messy* corpus — the analyze→decide→act loop | `category`, `product` |
| **03** | Support Docs (rich metadata) | 16 | Verifying metadata ingestion + every filter type works | `topic`, `type`, `product`, `priority` |
| **04** | API Discovery (Phase 1) | 30 | The real use case: discover *which* API does X | `domain`, `method`, `status` |
| **05** | API Schema (Phase 2) | 23 | The real use case: *how* to call an endpoint (params/body/response/errors) | `aspect`, `endpoint`, `domain` |

**01 → 02 → 03** build the core skill: see a clean space, learn to spot flaws in a
messy one, then confirm your metadata tooling works. **04 → 05** apply all of it to
your actual project — API discovery, then API schema detail. 04 and 05 chain together
(discover an endpoint, then answer schema questions about it) via the shared
`endpoint` metadata.

## The one workflow every dataset follows

Each README is organized the same way, because this is the loop you run on *any*
corpus at work:

1. **Ingestion** — load the data, embed the text, put the facets in metadata.
2. **Examination** — use Studio's Browse / Search / Visualize / Cluster views to
   understand and audit the collection.
3. **Enrichment** — the decisions each view surfaces: enrich content, dedupe, fix
   metadata, re-chunk, or add a filter field.

Learn the loop once here on small datasets you can see whole; apply it to real,
large corpora later.

## How to run any dataset's notebook

```bash
# from your chroma_lab_env (the venv with chromadb 1.5.9)
cd NN_name
jupyter notebook ingestion_examination.ipynb   # or open in VS Code
```
Every notebook defaults to an **offline mock embedder** so it runs with zero setup.
To use the real in-house Jina model (sharper retrieval), set `USE_MOCK = False` in
the setup cell — the metadata/filtering behavior is identical either way, only the
embedding quality changes.

Then open **Chroma Studio** (`../chroma_studio/` in your other deliverables), point
its sidebar at the folder the notebook created, and reproduce the examination steps
visually. The notebook is the "why"; Studio is the interactive "where you'd click."

## A note on the embedder for these datasets

The offline mock is deliberately crude (word-overlap), which is enough to demonstrate
metadata, filtering, clustering, and the examination loop — all of which are
embedder-independent. Semantic *retrieval quality* (which result ranks first) is where
the real Jina model matters most; the notebooks flag where the mock is approximate.
```
