# Milestones & Agent Prompts
## Mule API Semantic Detection & Composition Phase — Phase 2

**Prerequisite:** Phase 1 all milestones complete and validated.

---

## Milestone map

| # | Name | Depends on | Delivers |
|---|---|---|---|
| M3 | Vector Ingestion + Structured Fields | Phase 1 complete | node_embeddings + api_fields populated |
| M4 | Embedding Verification | M3 | UMAP gap confirmed > 0.10 |
| M5 | Field Mapping Precomputation | M3 | field_mappings table populated |
| M6 | Composition Validator (deterministic) | M4, M5 | Numeric scoring, composition_candidates |
| M6b | LLM Integration | M6 | All 4 LLM points wired, merge candidates back-filled |
| M9 | Streamlit: API Discovery | M6b | Screen 4 live |
| M11 | Streamlit: Composition Advisor + Embedding Health | M6b | Screens 5 and 6 live |

---

## M3 — Vector Ingestion + Structured Fields

**Goal:** Two things in one pass from re-extracted API docs:
1. `node_embeddings` — 3-4 prose chunks per API embedded and stored
2. `api_fields` — structured request/response fields per API

The nodes already exist from Phase 1. This is an augmentation pass —
update existing nodes, add fields and embeddings.

**Agent prompt:**
```
Phase 1 is complete. api_nodes and api_edges are already populated.
This milestone augments existing nodes with embeddings and structured fields.

TASK:
1. Read a JSON file of extended API documents (same project_names as
   Phase 1 but now including request_fields_structured and
   response_fields_structured per 01-srs.md Section 2).

2. For each document, call get_embedding() for each chunk type:
   - 'purpose':         "{purpose_text} {functionality}".strip()
   - 'request_fields':  prose from request_fields_structured field names/descriptions
   - 'response_fields': prose from response_fields_structured field names/descriptions

   Insert into node_embeddings with ON CONFLICT DO UPDATE.
   Wire get_embedding() to your internal LLM endpoint from .env.

3. For each document, parse request_fields_structured and
   response_fields_structured into api_fields rows:
   - field_path: the path value as-is (e.g. "debit.amount")
   - field_name: the leaf segment (everything after the last dot,
     strip [] from array notation: "items[].sku_id" -> field_name="sku_id")
   - direction: 'request' or 'response'
   - Insert with ON CONFLICT DO NOTHING

4. Populate api_specs with the raw JSON doc for each API.

5. After all embeddings inserted, build the HNSW index:
   CREATE INDEX idx_node_emb_hnsw ON node_embeddings
   USING hnsw (embedding vector_cosine_ops) WITH (m=16, ef_construction=64);

Print: embeddings inserted, api_fields rows, nodes missing structured fields.

[PASTE: 01-srs.md Section 2 source format]
[PASTE: 01-srs.md Section 4 chunking strategy table]
```

**Verify:**
```sql
-- Embedding coverage (expect ~3-4x node count)
SELECT COUNT(*) FROM node_embeddings;
SELECT COUNT(*) FROM node_embeddings WHERE chunk_type='purpose';
-- Must equal active node count

-- Every active node has a purpose embedding
SELECT n.project_name FROM api_nodes n
LEFT JOIN node_embeddings e ON e.node_id=n.node_id AND e.chunk_type='purpose'
WHERE n.status='active' AND e.embedding_id IS NULL;
-- Must return 0 rows

-- api_fields coverage (must be > 0)
SELECT direction, COUNT(*) FROM api_fields GROUP BY direction;

-- HNSW index built
SELECT indexname FROM pg_indexes WHERE tablename='node_embeddings';
```

---

## M4 — Embedding Verification

**Goal:** Confirm embeddings separate by domain before trusting similarity
scores. Gap must be > 0.10. If not, fix purpose_text quality, not the model.

**Agent prompt:**
```
Implement verify_embedding_distribution() that:
1. Reads all node_embeddings WHERE chunk_type='purpose'
   joined to api_nodes and domain_taxonomy for domain labels
2. Runs umap.UMAP(n_neighbors=15, min_dist=0.1, metric='cosine') to
   project to 2D
3. Saves the UMAP scatter plot colored by domain to
   /tmp/umap_phase2.png
4. Computes the numeric gap:
   - within-domain: mean cosine similarity between APIs in same domain
   - cross-domain: mean cosine similarity between APIs in different domains
   - gap = within - across
5. Prints all three numbers and whether gap > 0.10

If gap <= 0.10: print specific diagnosis:
  - Check purpose_text length distribution
    (SELECT AVG(LENGTH(purpose_text)) FROM api_nodes WHERE status='active')
  - If avg < 50 chars, purpose_text is too short - fix extraction prompt first
  - Do NOT adjust the embedding model

[PASTE: 01-srs.md Section 5 (retrieval queries) for reference]
```

**Verify:**
Gap > 0.10. If not, return to the extraction step and improve `purpose_text`
quality before proceeding. M5 and M6 are meaningless if the gap is too low.

---

## M5 — Field Mapping Precomputation

**Goal:** Precompute which fields from each API's response can feed each
other API's request (within the same domain). Result stored in
`field_mappings`.

**Agent prompt:**
```
Precompute field compatibility for all API pairs in the same domain.

TASK:
For every pair of active api_nodes (A, B) where A and B share the same
domain_id, compute whether A's response fields can feed B's request fields.

Use this logic:
  For each required request field of B (field_name, data_type):
    1. Exact match: if A has a response field with the same field_name
       -> match_type='exact_name', confidence=1.0
    2. Fuzzy match: if fuzz.ratio(field_a_name, field_b_name) >= 80
       -> match_type='fuzzy_name', confidence=0.80
    3. Skip pairs with fuzzy ratio < 80 (LLM handles 50-79 in M6b)
    4. Type compatibility: if both fields have data_type set,
       deduct 50% confidence if types are clearly incompatible
       (e.g. string vs integer)

Insert into field_mappings. Omit cross-domain pairs entirely.
Print: total pairs evaluated, rows inserted, average confidence.

Use python-Levenshtein or thefuzz for fuzzy matching.
Do NOT call the LLM in this milestone.

[PASTE: api_fields schema from 01-srs.md Section 2.6]
```

**Verify:**
```sql
-- Field mappings created
SELECT COUNT(*) FROM field_mappings;
SELECT match_type, COUNT(*) FROM field_mappings GROUP BY match_type;

-- Spot check: known field pair should exist
-- e.g. mandate_id in proc-nach-debit response
--   should map to mandate_id in sys-nach-clearance request
SELECT fm.confidence, fm.match_type,
       sf.field_name AS source_field,
       tf.field_name AS target_field,
       sn.project_name AS source_api,
       tn.project_name AS target_api
FROM field_mappings fm
JOIN api_fields sf ON sf.field_id = fm.source_field_id
JOIN api_fields tf ON tf.field_id = fm.target_field_id
JOIN api_nodes sn ON sn.node_id = fm.source_node_id
JOIN api_nodes tn ON tn.node_id = fm.target_node_id
WHERE sf.field_name = 'mandate_id'
LIMIT 5;
```

---

## M6 — Composition Validator (deterministic)

**Goal:** Implement `analyze_requirement(text, conn)` that uses
vector retrieval + field mappings + formula scoring to produce
composition candidates. NO LLM calls yet.

**Agent prompt:**
```
Implement the deterministic composition scoring pipeline in
core/composition.py. No LLM calls in this milestone.

TASK:
Implement analyze_requirement(requirement: str, conn) -> list[dict]:

Step 1: Embed the requirement text using get_embedding() from core/llm.py
        (implement the embedding call but not the chat completion calls)

Step 2: Run the semantic search from 01-srs.md Section 5 Use case 2
        to get top-5 candidate APIs ordered by cosine similarity

Step 3: For each single-API candidate:
        - similarity_score  = cosine similarity from step 2
        - schema_compat     = 1.0 (single API satisfies its own fields)
        - domain_alignment  = 1.0
        - composite         = composition_confidence(sim, 1.0, 1.0)

Step 4: For top-2 pair composition (API_A -> API_B):
        - schema_compat = schema_compat(A.node_id, B.node_id, conn)
          from 01-srs.md Section 6.1
        - domain_alignment = 1.0 if same domain else 0.60
        - composite = composition_confidence(avg_sim, schema_compat, domain_align)

Step 5: Band the best result:
        composite >= 0.85 and type=='single'  -> DIRECT_MATCH
        composite >= 0.60                     -> COMPOSE
        else                                  -> NEW_BUILD

Step 6: INSERT into composition_candidates with status='proposed'
        Leave llm_rationale NULL.

Return the top-3 results as a list of dicts.

[PASTE: 01-srs.md Sections 6.1, 6.2, 6.3]
```

**Verify:**
Run 3 test requirements manually:
1. A requirement you know matches one existing API exactly → DIRECT_MATCH
2. A requirement needing two APIs chained → COMPOSE
3. A requirement with no existing coverage → NEW_BUILD

All three band correctly. `llm_call_log` stays empty (no LLM yet).

---

## M6b — LLM Integration

**Goal:** Wire all 4 LLM points. Back-fill semantic scores and rationale
on existing Phase 1 `merge_candidates`. All calls logged to `llm_call_log`.

**Agent prompt:**
```
Implement core/llm.py with all 4 LLM integration points from
07-llm-integration-guide.md (Phase 1 full docs, or paste below).

TASK:

1. BASE CLIENT: call_llm(system, user, temperature, max_tokens) and
   get_embedding(text) — read INTERNAL_LLM_URL, INTERNAL_LLM_API_KEY,
   INTERNAL_LLM_MODEL from .env. Every call writes to llm_call_log
   via log_llm_call() before returning.

2. LLM POINT 1 - expand_query(query: str) -> list[str]:
   Expand to 3 semantic variants. Return [original] on any failure.
   Skip if query is > 10 words. temperature=0.3.

3. LLM POINT 2 - check_field_equivalence(field_a, type_a, field_b,
   type_b, domain) -> dict:
   Called ONLY from field_mappings where fuzzy confidence is 0.50-0.79.
   Return {equivalent, confidence, reason}. temperature=0.0.

4. LLM POINT 3 - make_composition_decision(requirement, candidates,
   field_mappings, formula_scores) -> dict:
   Reads formula scores as INPUT signals (not the decision).
   Returns {recommendation, confidence, target_apis, rationale, risks}.
   Update the composition_candidates row with llm_rationale. temperature=0.1.

5. LLM POINT 4 - quick_take_batch(query, apis, conn) -> list[dict]:
   One call per API card on Discovery screen. ThreadPoolExecutor(max_workers=5).
   Returns [{node_id, verdict: YES|PARTIAL|NO, note}]. temperature=0.0.

6. BACK-FILL POINT - backfill_merge_candidates(conn):
   For every merge_candidates row WHERE semantic_score IS NULL:
   - Get purpose embeddings for node_a and node_b from node_embeddings
   - Compute cosine similarity -> set semantic_score
   - Call LLM for rationale -> set llm_rationale
   - UPDATE merge_candidates SET semantic_score=..., llm_rationale=...
   Run this ONCE after wiring. After this, Screen 3 shows full rationale.

Graceful fallback: every LLM point must work (with degraded quality)
if INTERNAL_LLM_URL is unreachable. Never crash the UI on LLM failure.

[PASTE: 07-llm-integration-guide.md full content]
```

**Verify:**
```python
from core.llm import expand_query, check_field_equivalence, call_llm
from core.db import get_conn

conn = get_conn()

# Point 1: query expansion
variants = expand_query("mandate debit")
assert len(variants) >= 2, "Must return original + at least 1 variant"

# Point 2: field equivalence
result = check_field_equivalence("mandate_id","string","mandate_ref","string","payments")
assert 'equivalent' in result

# Back-fill: all merge candidates have llm_rationale
with conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM merge_candidates WHERE llm_rationale IS NULL")
    null_count = cur.fetchone()[0]
print(f"Merge candidates still missing rationale: {null_count}  (expected 0)")

# LLM call log has entries
with conn.cursor() as cur:
    cur.execute("SELECT call_type, COUNT(*) FROM llm_call_log GROUP BY call_type")
    log_summary = cur.fetchall()
print("llm_call_log entries:", log_summary)
```

---

## M9 — Streamlit: API Discovery

**Goal:** Screen 4 live — unified search, 3 modes auto-detected, async LLM
quick-take badges.

**Agent prompt:**
```
Build app/4_API_Discovery.py exactly as specified in Phase 2
03-ui-design.md Section "Screen 4 — API Discovery".

Key requirements:
1. detect_mode() uses snake_case regex for field detection
2. search_apis() tries taxonomy BEFORE semantic — if taxonomy_search()
   returns results, skip the semantic search entirely
3. LLM query expansion runs BEFORE semantic search, not after
4. Quick-takes (LLM Point 4) run in a background thread — search results
   must render immediately without waiting for LLM responses
5. Empty-state must include a visible link/button to Screen 5
   (Composition Advisor)
6. "View detail" button uses st.session_state + st.switch_page to
   navigate to Screen 1 (Graph Explorer) with the node pre-selected

Add search functions to core/search.py:
  search_apis, detect_mode, run_semantic_search,
  run_field_search, run_taxonomy_search, get_all_domains

[PASTE: Phase 2 03-ui-design.md Screen 4 full code]
```

**Verify:**
- `mandate_id` (snake_case) → field search mode, returns APIs with that field
- `payments` → taxonomy mode, returns all payments domain APIs
- `process recurring NACH debit` → semantic mode, nach APIs at top
- Submit with no results → empty-state link to Composition Advisor visible
- Quick-take badges appear ~2-3 sec after results, without blocking render

---

## M11 — Streamlit: Composition Advisor + Embedding Health

**Goal:** Screens 5 and 6 live. Composition Advisor shows LLM rationale
and field mapping table. Embedding Health shows UMAP plot and gap metric.

**Agent prompt:**
```
Build app/5_Composition_Advisor.py and app/6_Embedding_Health.py exactly
as specified in Phase 2 03-ui-design.md Screens 5 and 6.

Composition Advisor requirements:
1. On submit: call composition.analyze_requirement(requirement, conn)
   which runs the full 4-step pipeline (embed, retrieve, score, LLM decision)
2. Show results grouped by band: DIRECT_MATCH (green), COMPOSE (orange),
   NEW_BUILD (red)
3. For COMPOSE results: show the field mapping detail table from
   composition.get_field_mappings(node_a_id, node_b_id, conn)
   Rows where satisfied=False AND is_required=True must be highlighted RED
4. Approve/Reject writes to BOTH composition_candidates AND audit_log
   in a single transaction. Comment required.
5. Never show a single blended accuracy percentage — only per-result
   breakdown (similarity, schema, domain, composite separately)

Embedding Health requirements:
1. chunk_type selector: purpose, business_rules, request_fields, response_fields
2. UMAP plot renders in st.pyplot() - handle ImportError for umap-learn gracefully
3. Numeric gap displayed as st.metric() with delta indicator (green if > 0.10)
4. Coverage table: nodes WITH purpose embedding vs total active nodes
5. List any nodes missing purpose embedding (these will not appear in search)

[PASTE: Phase 2 03-ui-design.md Screens 5 and 6 full code]
```

**Verify:**
- Type a requirement that matches a known NACH debit API → DIRECT_MATCH
- Type a requirement needing mandate validate + nach debit → COMPOSE
  Field mapping table appears, shows which fields are satisfied
- Type a requirement with no existing coverage → NEW_BUILD
- Embedding Health: gap metric matches M4 output
- Approve one composition candidate → status='approved', audit_log row present

---

## What comes after Phase 2

Phase 2 completes the platform. The governance process is now:

```
Developer searches API Discovery
    -> Direct match: use existing API
    -> No match: Composition Advisor
        -> COMPOSE: raise design for new Proc orchestrator
        -> NEW_BUILD: proceed with new development

New API ingested on weekly refresh
    -> Structural Detection flags any redundancy (Phase 1 rules)
    -> Semantic Detection adds LLM merge scoring
    -> Architect reviews in Findings Dashboard / Merge Candidates
    -> Composition Advisor updated with new API as a candidate

Ongoing
    -> Embedding Health confirms vectors stay well-separated
    -> Validation notebooks confirm quality thresholds still met
    -> audit_log provides governance evidence trail
```

Future enhancements (no schema changes needed):
- API lifecycle states (draft -> approved -> active -> deprecated -> retired)
- Consumer registry (business app -> API dependency mapping)
- Standards compliance checker (auto-flag missing purpose/fields/team)
- New API request gate (pre-build composition check)
