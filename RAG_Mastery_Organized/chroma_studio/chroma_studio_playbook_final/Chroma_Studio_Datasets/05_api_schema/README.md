# API Schema (Phase 2)

The real use case, part 2: answer HOW to call an endpoint — its parameters, body, response, and errors. One endpoint becomes SEVERAL aspect-chunks.

**Dataset:** `dataset/api_schema_chunks.csv` — 23 rows
**Metadata fields:** `aspect (params/request/response/errors)`, `endpoint`, `method`, `domain`

## What this dataset teaches
Aspect-scoped chunking: split each endpoint into params/request/response/errors chunks so schema questions retrieve exactly the relevant piece. The `aspect` field is a first-class filter. Chains to Phase 1 via `endpoint`.

---

## 1. Ingestion
1. Load `api_schema_chunks.csv` (SEVERAL rows per endpoint, one per aspect).
2. Embed each aspect chunk's `text` separately.
3. Put aspect/endpoint/method/domain/version/status into metadata — `aspect` is the key new field.
4. Ingest into a collection named `api_schema` (separate from Phase 1's collection).

Run `ingestion_examination.ipynb` in this folder — it does the ingestion above and
then walks the examination below. It defaults to an offline mock embedder so it runs
immediately; set `USE_MOCK = False` (or swap in `InHouseEmbeddings()`) for the real
in-house Jina model, which sharpens retrieval quality.

To regenerate or tweak the dataset itself, run `dataset/build_dataset.py`.

## 2. Examination in Chroma Studio
Point Chroma Studio's sidebar at this collection's folder, then:

- **Browse → filter `aspect = errors`** — Every error chunk across all endpoints — an 'all error codes' audit in one view.
- **Visualize → color by `aspect`** — params/request/response/errors form four families.
- **Browse → filter `endpoint = /v1/payments/{id}/refund`** — The 4 chunks of that endpoint's schema.
- **Visualize → color by `domain`, filter `aspect = request`** — Compare request-body shapes across domains.

The notebook computes the same things in code (so you understand what each view
shows); Studio is the interactive version of the same checks.

## 3. Enrichment — decisions this dataset lets you practice
- Add a `required` boolean or `deprecated_fields` note per request chunk.
- Chain with Phase 1: use discovery to find the endpoint, then filter this collection by that `endpoint` + `aspect` to answer schema follow-ups.
- Add Phase-2 coverage for more endpoints by extending `build_dataset.py`.

Enrichment via metadata (Edit/Update tab) is instant — a metadata-only change does
NOT re-embed. Only changing a document's **text** triggers re-embedding.

---

*Part of the Chroma Studio Datasets collection. See `../_guide/` for the full feature
guide and `../README.md` for the learning order across all five datasets.*
