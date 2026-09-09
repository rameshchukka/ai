# Architecture Guide
## Mule API Semantic Detection & Composition Phase — Phase 2

**Changes from Phase 1:** pgvector now populated, internal LLM wired,
4 new screens added.

---

## 1. What changes vs Phase 1

| Concern | Phase 1 | Phase 2 |
|---|---|---|
| Vector store | pgvector installed, empty | pgvector populated (node_embeddings) |
| LLM | None | Internal endpoint, 4 integration points |
| Screens | 3 | 7 (add API Discovery, Composition Advisor, Embedding Health) |
| Field data | Not ingested | api_fields populated from structured extraction |

Everything else is unchanged — same PostgreSQL instance, same Streamlit
framework, same core/ package extended with new modules.

---

## 2. pgvector: why inside PostgreSQL, not a separate DB

This decision was made in the full design and applies here.
The single reason that matters: composition queries need vector similarity
AND relational filters in the same query:

```sql
-- Find APIs similar to a requirement, filtered to active nodes in one domain
SELECT n.project_name,
       1 - (e.embedding <=> :req_vec::vector) AS similarity
FROM node_embeddings e
JOIN api_nodes n ON n.node_id = e.node_id
JOIN domain_taxonomy dt ON dt.domain_id = n.domain_id
WHERE e.chunk_type = 'purpose'
  AND n.status = 'active'
  AND dt.domain_name = 'payments'
ORDER BY e.embedding <=> :req_vec::vector
LIMIT 5;
```

With a separate vector DB (ChromaDB, Pinecone) this is two round-trips
plus application-layer join. With pgvector it is one SQL query.

---

## 3. LLM: 4 integration points, not a replacement for determinism

```
Developer types requirement
        |
        v
[LLM POINT 1] Query Expansion    -- expand short queries to 3 variants
        |
        v
[SQL] Vector retrieval            -- cosine search node_embeddings
        |
        v
[SQL] Schema compatibility        -- field_mappings lookup (deterministic)
        |
[LLM POINT 2] Field Equivalence  -- only for 0.50-0.79 fuzzy matches
        |
        v
[Python] Composite score formula  -- 0.40*sim + 0.35*schema + 0.25*domain
        |
[LLM POINT 3] Composition decision -- reads formula scores, decides band
        |
        v
Result rendered on screen
        |
[LLM POINT 4] Discovery quick-take -- async YES/PARTIAL/NO badge (Discovery screen)
```

LLM is NOT used for graph traversal, structural rules, exact field
matching, taxonomy lookup, or audit writes. Those stay deterministic.

---

## 4. Extended project structure

```
project/
├── core/
│   ├── db.py           -- unchanged from Phase 1
│   ├── graph.py        -- unchanged from Phase 1
│   ├── traversal.py    -- unchanged from Phase 1
│   ├── rules.py        -- unchanged from Phase 1
│   ├── vector_store.py -- NEW: pgvector ingestion + retrieval
│   ├── composition.py  -- NEW: field mapping, scoring, analysis
│   ├── search.py       -- NEW: 3-mode API Discovery search
│   └── llm.py          -- NEW: 4 LLM points + llm_call_log
├── app/
│   ├── 1_Graph_Explorer.py      -- unchanged from Phase 1
│   ├── 2_Findings_Dashboard.py  -- unchanged from Phase 1
│   ├── 3_Merge_Impact.py        -- updated: llm_rationale now visible
│   ├── 4_API_Discovery.py       -- NEW
│   ├── 5_Composition_Advisor.py -- NEW
│   └── 6_Embedding_Health.py    -- NEW
├── scripts/
│   ├── ingest.py         -- extended: adds fields + embeddings pass
│   ├── ingest_fields.py  -- NEW: structured field augmentation pass
│   └── refresh.py        -- unchanged from Phase 1
└── .env                  -- extended: add LLM endpoint vars
```

---

## 5. `.env` additions for Phase 2

```bash
# Add to existing Phase 1 .env:
INTERNAL_LLM_URL=https://your-internal-llm.company.com/v1/chat/completions
INTERNAL_LLM_API_KEY=your-key-here
INTERNAL_LLM_MODEL=gpt-4o
INTERNAL_LLM_EMBED_URL=https://your-internal-llm.company.com/v1/embeddings
INTERNAL_LLM_EMBED_MODEL=text-embedding-3-small
EMBED_DIM=1536
```

---

## 6. Merge Candidates screen update (Screen 3)

Screen 3 from Phase 1 showed `llm_rationale` as "pending". In Phase 2,
after M6b back-fills semantic scores, the screen should show:
- `structural_score` — already set
- `semantic_score` — now populated
- `llm_rationale` — now populated
- Combined confidence = weighted blend of both scores

No structural code change needed — the column values just go from NULL
to populated. The display logic already checks for NULL and shows "pending".

---

## 7. Summary table

| Decision | Phase 1 | Phase 2 addition |
|---|---|---|
| Vector store | pgvector created, empty | pgvector populated, HNSW index built |
| LLM | None | 4 integration points, all calls logged |
| Field data | Not ingested | api_fields populated from re-extraction pass |
| Screens | 3 | +3 more (API Discovery, Composition, Embedding Health) |
| Merge candidates | Structural score only | + semantic score + LLM rationale |
