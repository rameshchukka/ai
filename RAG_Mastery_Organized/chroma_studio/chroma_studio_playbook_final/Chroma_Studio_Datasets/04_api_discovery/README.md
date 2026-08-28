# API Discovery (Phase 1)

The real use case, part 1: discover WHICH API does something from a plain-language query. One row per endpoint, embed its purpose.

**Dataset:** `dataset/api_catalog.csv` — 30 rows
**Metadata fields:** `domain (7 services)`, `method`, `version`, `status`

## What this dataset teaches
Discovery by intent: embed each endpoint's PURPOSE (not its URL), filter by `domain` and `method`. Planted structure (v1/v2 duplicate, deprecated endpoint, a collision) surfaces real API-catalog decisions.

---

## 1. Ingestion
1. Load `api_catalog.csv` (one row per endpoint; columns include text=purpose, endpoint, method, domain, auth, version, status).
2. Embed the `text` (purpose) — this is what makes intent-based discovery work.
3. Put endpoint/method/domain/auth/version/status into metadata.
4. Ingest into a collection named `api_catalog`.

Run `ingestion_examination.ipynb` in this folder — it does the ingestion above and
then walks the examination below. It defaults to an offline mock embedder so it runs
immediately; set `USE_MOCK = False` (or swap in `InHouseEmbeddings()`) for the real
in-house Jina model, which sharpens retrieval quality.

To regenerate or tweak the dataset itself, run `dataset/build_dataset.py`.

## 2. Examination in Chroma Studio
Point Chroma Studio's sidebar at this collection's folder, then:

- **Search → 'refund a payment'** — `pay_refund_01` (POST /v1/payments/{id}/refund) on top.
- **Browse → filter `domain = payments`** — 6 endpoints.
- **Visualize → color by `domain`** — Domains cluster; spot the cross-domain overlap (a notifications endpoint living at a customer path).
- **Visualize → stacked points** — pay_create v1 and v2 sit together — versioning decision.
- **Browse → filter `status = deprecated`** — The legacy /v1/login — exclude from discovery.

The notebook computes the same things in code (so you understand what each view
shows); Studio is the interactive version of the same checks.

## 3. Enrichment — decisions this dataset lets you practice
- Add a `team` or `owner` metadata field per domain, then filter discovery by team.
- Decide the versioning policy: filter `version = v2` at query time so discovery returns only the latest create-payment.
- Fix the notification/webhook collision by adding a discriminating field (e.g. `pattern: push` vs `pattern: webhook`).

Enrichment via metadata (Edit/Update tab) is instant — a metadata-only change does
NOT re-embed. Only changing a document's **text** triggers re-embedding.

---

*Part of the Chroma Studio Datasets collection. See `../_guide/` for the full feature
guide and `../README.md` for the learning order across all five datasets.*
