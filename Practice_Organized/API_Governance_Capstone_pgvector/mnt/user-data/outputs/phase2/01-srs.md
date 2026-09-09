# Software Requirements Specification
## Mule API Semantic Detection & Composition Phase — Phase 2

**Prerequisite:** Phase 1 (Structural Detection) fully live and validated.
All 19 tables already exist. This phase populates the reserved tables.

**What this phase adds:**
1. Semantic Detection — LLM-assisted merge candidate scoring
2. API Discovery — 3-mode developer search
3. Composition Advisor — DIRECT_MATCH / COMPOSE / NEW_BUILD
4. Embedding Health monitoring

---

## 1. Tables activated in this phase

All tables were created in Phase 1 M1. This phase populates the ones
that were Reserved:

| Table | Phase 2 status | Populated in |
|---|---|---|
| `functionality_taxonomy` | Now populated | M3 (taxonomy expansion) |
| `api_fields` | Now populated | M3 (structured field extraction) |
| `node_embeddings` | Now populated | M3 (vector ingestion) |
| `api_specs` | Now populated | M3 (raw source storage) |
| `field_mappings` | Now populated | M5 (precomputation) |
| `composition_candidates` | Now populated | M6 (composition advisor) |
| `llm_call_log` | Now populated | M6b (all LLM calls logged) |

Existing Phase 1 tables that gain new data:
| Table | What is added |
|---|---|
| `merge_candidates` | `semantic_score` + `llm_rationale` back-filled by M6b |
| `structural_findings` | No change — Phase 1 findings remain as-is |

---

## 2. Source data format extension

Phase 1 required only:
```json
{ "project_name", "layer", "domain", "purpose_text", "calls[]", ... }
```

Phase 2 requires the same document extended with structured fields:

```json
{
  "project_name":      "proc-nach-debit-api",
  "layer":             "proc",
  "domain":            "payments",
  "functionality":     "NACH Debit Processing",
  "owning_team":       "payments-team",
  "listener_endpoint": "/proc/v1/nach/debit/initiate",
  "purpose_text":      "Orchestrates NACH debit - validates mandate and submits to clearance.",
  "repo_name":         "mule-proc-nach-debit",
  "calls": [...],

  "request_fields_structured": [
    {"path": "mandate_id",          "type": "string",  "required": true,
     "description": "Mandate identifier", "example": "MND-001"},
    {"path": "debit.amount",        "type": "decimal", "required": true,
     "description": "Debit amount",       "example": "5000.00"},
    {"path": "debit.currency",      "type": "string",  "required": true,
     "description": "ISO 4217 code",      "example": "INR"},
    {"path": "bank.account_number", "type": "string",  "required": true,
     "description": "Bank account",       "example": "1234567890"},
    {"path": "bank.ifsc_code",      "type": "string",  "required": true,
     "description": "Bank IFSC",          "example": "HDFC0001234"}
  ],

  "response_fields_structured": [
    {"path": "transaction_id",      "type": "string",   "required": true,
     "description": "Clearance TX ID",    "example": "CLR-001"},
    {"path": "status",              "type": "string",   "required": true,
     "description": "SUBMITTED|FAILED",   "example": "SUBMITTED"},
    {"path": "mandate_id",          "type": "string",   "required": true,
     "description": "Echo of input",      "example": "MND-001"}
  ]
}
```

**Field path notation:**
- `mandate_id` — top-level field, `field_name = mandate_id`
- `debit.amount` — nested object, `field_name = amount` (leaf only)
- `bank.ifsc_code` — nested object, `field_name = ifsc_code`
- `items[].sku_id` — array element, `field_name = sku_id`

The composition validator matches on `field_name` (the leaf), not the full
path. So `debit.amount` and `entry.amount` both have `field_name = amount`
and satisfy each other.

---

## 3. pgvector setup

```sql
-- Already created in Phase 1 M1. Confirm it is active:
SELECT * FROM pg_extension WHERE extname = 'vector';

-- node_embeddings table already exists. Build HNSW index after bulk insert:
CREATE INDEX IF NOT EXISTS idx_node_emb_hnsw
    ON node_embeddings
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
```

> Build the HNSW index AFTER bulk insert, not before. Building per-row
> during insert is significantly slower.

---

## 4. Chunking strategy

| Source field(s) | Chunk type | Embedded |
|---|---|---|
| `purpose_text` + `functionality` | `purpose` | Yes |
| `business_rules` (if available) | `business_rules` | Yes |
| `request_fields_structured` (as prose) | `request_fields` | Yes |
| `response_fields_structured` (as prose) | `response_fields` | Yes |

Each API produces 3-4 chunks. At ~700 APIs: ~2,100-2,800 rows in
`node_embeddings`.

---

## 5. Retrieval queries (pgvector)

### Use case 1: Functional redundancy (semantic similarity)

```sql
SELECT
    n.node_id, n.project_name, n.layer, n.domain,
    1 - (e.embedding <=> :query_vec::vector) AS similarity
FROM node_embeddings e
JOIN api_nodes n ON n.node_id = e.node_id
WHERE e.chunk_type = 'purpose'
  AND n.status = 'active'
  AND e.node_id <> :source_node_id
ORDER BY e.embedding <=> :query_vec::vector
LIMIT 10;
```

### Use case 2: New requirement matching (composition)

```sql
SELECT
    n.node_id, n.project_name, n.layer, n.domain, n.functionality,
    1 - (e.embedding <=> :req_vec::vector) AS similarity
FROM node_embeddings e
JOIN api_nodes n ON n.node_id = e.node_id
WHERE e.chunk_type = 'purpose'
  AND n.status = 'active'
ORDER BY e.embedding <=> :req_vec::vector
LIMIT 5;
```

### Use case 3: Domain-filtered search (composition within domain)

```sql
SELECT
    n.node_id, n.project_name, n.layer,
    1 - (e.embedding <=> :req_vec::vector) AS similarity
FROM node_embeddings e
JOIN api_nodes n ON n.node_id = e.node_id
JOIN domain_taxonomy dt ON dt.domain_id = n.domain_id
WHERE e.chunk_type = 'purpose'
  AND n.status = 'active'
  AND dt.domain_name = :domain_name
ORDER BY e.embedding <=> :req_vec::vector
LIMIT 5;
```

---

## 6. Composition validator

### 6.1 Schema compatibility scoring

For a proposed composition A → B (A's response feeds B's request):

```python
def schema_compat(source_node_id: int, target_node_id: int, conn) -> float:
    """Fraction of target's required request fields satisfied by
    source's response fields (leaf-name matching)."""
    with conn.cursor() as cur:
        cur.execute(\"\"\"
            SELECT field_name FROM api_fields
            WHERE node_id=%s AND direction='response'
        \"\"\", (source_node_id,))
        src_leaves = {r[0] for r in cur.fetchall()}

        cur.execute(\"\"\"
            SELECT field_name, is_required FROM api_fields
            WHERE node_id=%s AND direction='request'
        \"\"\", (target_node_id,))
        tgt_required = [(r[0], r[1]) for r in cur.fetchall()]

    required = [f for f, req in tgt_required if req]
    if not required:
        return 1.0
    satisfied = sum(1 for f in required if f in src_leaves)
    return round(satisfied / len(required), 4)
```

### 6.2 Composite confidence score

```python
def composition_confidence(similarity: float,
                            schema_compat: float,
                            domain_alignment: float) -> float:
    return round(
        0.40 * similarity +
        0.35 * schema_compat +
        0.25 * domain_alignment,
        4
    )
```

### 6.3 Recommendation bands

| Composite score | Recommendation |
|---|---|
| >= 0.85 (single API) | DIRECT_MATCH |
| >= 0.60 | COMPOSE |
| < 0.60 | NEW_BUILD |

---

## 7. LLM integration points (4 total)

All LLM calls log to `llm_call_log` before returning.

### Point 1: Query expansion (before vector retrieval)

Expands a short query into 3 semantic variants.
Skips if query is > 10 words or matches a known taxonomy term.

### Point 2: Field equivalence (supplement to SQL, ambiguous zone only)

Called only when SQL fuzzy match confidence is 0.50–0.79.
`temperature = 0.0` for determinism.

### Point 3: Composition decision (primary decision maker)

Reads formula scores + candidate context. Returns structured JSON:
`{recommendation, confidence, target_apis, rationale, risks}`.
`temperature = 0.1`.

### Point 4: Discovery quick-take (async secondary reviewer)

Per result card on the API Discovery screen. Returns YES/PARTIAL/NO.
Runs in parallel via `ThreadPoolExecutor(max_workers=5)`.
`temperature = 0.0`.

### Back-fill Point: Semantic merge scoring

For existing Phase 1 `merge_candidates` rows:
- Embed purpose text of node_a and node_b
- Compute cosine similarity
- Call LLM for rationale
- UPDATE merge_candidates SET semantic_score=..., llm_rationale=...

---

## 8. Open decisions carried forward from Phase 1

- `DEEP_CHAIN_THRESHOLD = 4` — unchanged
- `FAN_IN_THRESHOLD = 3` — unchanged
- `DIRECT_MATCH_THRESHOLD = 0.85` — tune after first labelled test set
- `COMPOSE_THRESHOLD = 0.60` — tune after architect review
- Composition formula weights (0.40/0.35/0.25) — tune after first 20 reviews
