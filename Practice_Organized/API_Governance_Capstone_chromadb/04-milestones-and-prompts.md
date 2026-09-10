# Milestones & Agent Prompts — Phase 2 (ChromaDB variant)
## Mule API Semantic Detection & Composition Phase

**Prerequisite:** Phase 1 all milestones complete and validated.

**Key difference from pgvector variant:** M3 populates ChromaDB instead of
`node_embeddings` PostgreSQL table. M4 reads from ChromaDB for verification.
M6b uses ChromaDB for retrieval. All other milestones are identical.

---

## Milestone map

| # | Name | Depends on | Delivers |
|---|---|---|---|
| M3 | ChromaDB Ingestion + Structured Fields | Phase 1 complete | ChromaDB populated + api_fields |
| M4 | Embedding Verification | M3 | UMAP gap confirmed > 0.10 from ChromaDB |
| M5 | Field Mapping Precomputation | M3 | field_mappings populated |
| M6 | Composition Validator (deterministic) | M4, M5 | Numeric scoring, composition_candidates |
| M6b | LLM Integration | M6 | 4 LLM points wired, ChromaDB retrieval used |
| M9 | Streamlit: API Discovery | M6b | Screen 4 live |
| M11 | Streamlit: Composition Advisor + Embedding Health | M6b | Screens 5 and 6 live |

---

## M3 — ChromaDB Ingestion + Structured Fields

**Goal:** Two outputs from one pass over the extended API documents:
1. ChromaDB collection `api_knowledge` populated with 3-4 chunks per API
2. `api_fields` PostgreSQL table populated with structured field rows

**Agent prompt:**
```
Phase 1 is complete. api_nodes and api_edges are already in PostgreSQL.
This milestone adds embeddings to ChromaDB and structured fields to PostgreSQL.

TASK:

Step 1 - Setup ChromaDB:
  import chromadb
  client = chromadb.PersistentClient(path=os.getenv("CHROMA_PATH","./chroma_data"))
  collection = client.get_or_create_collection(
      name=os.getenv("CHROMA_COLLECTION","api_knowledge"),
      metadata={"hnsw:space": "cosine"}
  )

Step 2 - For each extended API document:
  a) Build prose chunks per 01-srs.md Section 4 (purpose, business_rules,
     request_fields, response_fields)
  b) Call get_embedding(text) from core/llm.py for each chunk
  c) Call collection.upsert() with ids, documents, embeddings, metadatas
     Metadata must include: node_id (int), project_name, layer, domain,
     domain_id (int), functionality, chunk_type, status="active"
  d) Parse request_fields_structured and response_fields_structured into
     api_fields rows (field_path, field_name=leaf, data_type, is_required)
     Insert into PostgreSQL api_fields table.
  e) Store raw JSON in api_specs PostgreSQL table.

Step 3 - After all chunks upserted, verify:
  print(collection.count())   # must be ~3-4x node count

DO NOT insert into node_embeddings PostgreSQL table — that table stays
empty in the ChromaDB variant.

[PASTE: 01-srs.md Phase 2 Section 4 chunking strategy]
[PASTE: 01-srs.md Phase 2 Section 5 ChromaDB ingestion code]
```

**Verify:**
```python
import chromadb
client     = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection("api_knowledge",
                metadata={"hnsw:space":"cosine"})

total     = collection.count()
node_count = # SELECT COUNT(*) FROM api_nodes WHERE status='active'

print(f"ChromaDB documents: {total}")
print(f"Ratio: {total/node_count:.1f}x per node (expected 3-4x)")

# Test retrieval works
results = collection.query(
    query_texts=["NACH debit mandate payment"],
    n_results=3,
    where={"chunk_type": {"$eq": "purpose"}}
)
print("Top 3 purpose matches:")
for i, meta in enumerate(results["metadatas"][0]):
    print(f"  {meta['project_name']}  dist={results['distances'][0][i]:.3f}")

# PostgreSQL field coverage
# SELECT COUNT(*) FROM api_fields;  -- must be > 0
# SELECT COUNT(*) FROM node_embeddings;  -- must be 0 (stays empty)
```

---

## M4 — Embedding Verification (ChromaDB)

**Goal:** Confirm ChromaDB embeddings separate by domain. Gap must be > 0.10.

**Agent prompt:**
```
M3 is complete. ChromaDB collection is populated.
Verify embedding quality by pulling all purpose embeddings from ChromaDB.

TASK:
1. Get all purpose chunk embeddings from ChromaDB:
   results = collection.get(
       where={"$and": [{"chunk_type":{"$eq":"purpose"}},
                        {"status":{"$eq":"active"}}]},
       include=["embeddings","metadatas"]
   )
   embeddings = results["embeddings"]
   domains    = [m["domain"] for m in results["metadatas"]]

2. Compute numeric gap:
   - within-domain: mean cosine similarity between APIs in same domain
   - cross-domain:  mean cosine similarity between APIs in different domains
   - gap = within - across
   Print all three values.

3. Run UMAP projection and save plot to /tmp/umap_chromadb.png

4. If gap <= 0.10:
   Print diagnosis: check average purpose_text length.
   SELECT AVG(LENGTH(purpose_text)) FROM api_nodes WHERE status='active'
   If avg < 50 chars: purpose text is too short -- fix extraction prompt.
   Do NOT change the embedding model.
```

**Verify:** Gap > 0.10 before proceeding to M5.

---

## M5 — Field Mapping Precomputation

**Identical to pgvector variant.** ChromaDB is not involved.
Field mappings are precomputed from `api_fields` PostgreSQL table.

**Agent prompt:**
```
[Same as pgvector variant 04-milestones-and-prompts.md M5 prompt]
No ChromaDB calls in this milestone.
```

---

## M6 — Composition Validator (deterministic)

**Goal:** `analyze_requirement(text, conn)` using ChromaDB retrieval +
field_mappings scoring. No LLM calls yet.

**Agent prompt:**
```
Implement the deterministic composition scoring pipeline using ChromaDB
for retrieval and PostgreSQL for field compatibility.

TASK:
Step 1: Embed the requirement using get_embedding() from core/llm.py

Step 2: Search ChromaDB for top-5 candidates:
  from core.vector_store import search_purpose
  candidates = search_purpose(query_vec, top_k=5)
  -- Returns list of {node_id, project_name, layer, domain, similarity}

Step 3: For each candidate, fetch relational fields from PostgreSQL:
  SELECT domain_id, owning_team, status FROM api_nodes WHERE node_id=%s
  This two-step pattern (ChromaDB then PostgreSQL) is necessary because
  ChromaDB metadata only stores what was put in at ingestion time.

Step 4: Score candidates using composition_confidence() formula from
  01-srs.md Phase 2 Section 7.

Step 5: Band and INSERT into composition_candidates with llm_rationale=NULL.

Note: the two-step retrieval (ChromaDB + PostgreSQL) is abstracted in
core/vector_store.py search_purpose() which already joins the metadata
from ChromaDB with any additional PostgreSQL lookup needed.

[PASTE: Phase 2 01-srs.md Sections 6 and 7]
```

**Verify:**
Run 3 test requirements. All three band correctly.
`llm_call_log` stays empty. `node_embeddings` PostgreSQL table stays 0 rows.

---

## M6b — LLM Integration (ChromaDB retrieval)

**Goal:** Wire all 4 LLM points using ChromaDB for vector retrieval.
Back-fill semantic scores on Phase 1 merge_candidates.

**Agent prompt:**
```
Implement core/llm.py with all 4 LLM integration points.
ChromaDB is used for retrieval — NOT the node_embeddings PostgreSQL table.

TASK:

1. BASE CLIENT: call_llm() and get_embedding() — read from .env.
   Every call writes to llm_call_log PostgreSQL table.

2. LLM POINT 1 - expand_query(query):
   Same as pgvector variant. Returns list of query variants.

3. LLM POINT 2 - check_field_equivalence():
   Same as pgvector variant. PostgreSQL field_mappings only.

4. LLM POINT 3 - make_composition_decision():
   Retrieval uses ChromaDB via core/vector_store.search_purpose().
   Then fetches relational data from PostgreSQL for each returned node_id.
   Formula scores passed to LLM. Returns {recommendation, rationale, ...}.

5. LLM POINT 4 - quick_take_batch():
   Same as pgvector variant. One LLM call per result card async.

6. BACK-FILL - backfill_merge_candidates(conn):
   For each merge_candidates row WHERE semantic_score IS NULL:
   - Get purpose text from ChromaDB:
     results = collection.get(
         ids=[f"{node_a_id}_purpose", f"{node_b_id}_purpose"],
         include=["embeddings"]
     )
   - Compute cosine similarity between the two embeddings
   - Call LLM for rationale
   - UPDATE merge_candidates SET semantic_score=..., llm_rationale=...

[PASTE: 07-llm-integration-guide.md full content]
```

**Verify:**
```python
from core.vector_store import get_collection, search_purpose
from core.llm import expand_query, get_embedding

# ChromaDB accessible
coll = get_collection()
print(f"ChromaDB docs: {coll.count()}")

# Retrieval works
vec      = get_embedding("NACH mandate debit")
results  = search_purpose(vec, top_k=3)
for r in results:
    print(f"  {r['similarity']:.3f}  {r['project_name']}")

# Query expansion
variants = expand_query("mandate debit")
print(f"Variants: {variants}")

# Back-fill done
# SELECT COUNT(*) FROM merge_candidates WHERE llm_rationale IS NULL;
# Must be 0
```

---

## M9 — Streamlit: API Discovery

**Identical to pgvector variant except retrieval uses ChromaDB.**

The `search_apis()` function in `core/search.py` calls
`core/vector_store.search_purpose()` for semantic search instead of
the pgvector SQL query. All other logic — detect_mode(), field search,
taxonomy search, quick-takes — is identical.

**Agent prompt:**
```
Build app/4_API_Discovery.py per 03-ui-design.md Screen 4.

Key difference from pgvector variant:
- run_semantic_search() calls core/vector_store.search_purpose(vec, top_k)
  which queries ChromaDB, then fetches supplementary fields from PostgreSQL
  for each returned node_id
- Do NOT use pgvector SQL (<=> operator) anywhere in this screen

Everything else is identical to the pgvector variant prompt.

[PASTE: Phase 2 03-ui-design.md Screen 4 full code]
```

---

## M11 — Streamlit: Composition Advisor + Embedding Health

**Composition Advisor:** Identical to pgvector variant. Retrieval is
abstracted in `core/composition.analyze_requirement()` which calls
`core/vector_store.search_purpose()`.

**Embedding Health — ChromaDB version:**

```python
# app/6_Embedding_Health.py — pull from ChromaDB, not node_embeddings table
from core.vector_store import get_collection
import numpy as np

coll    = get_collection()
results = coll.get(
    where={"$and": [
        {"chunk_type": {"$eq": chunk_type}},
        {"status":     {"$eq": "active"}}
    ]},
    include=["embeddings", "metadatas"]
)
embeddings = np.array(results["embeddings"])
domains    = [m["domain"] for m in results["metadatas"]]
```

All other Embedding Health logic (UMAP, gap metric, coverage count)
is identical to the pgvector variant.

**Agent prompt:**
```
Build app/5_Composition_Advisor.py and app/6_Embedding_Health.py
per Phase 2 03-ui-design.md Screens 5 and 6.

Key difference for Embedding Health:
- Pull embeddings from ChromaDB (core/vector_store.get_collection().get())
  NOT from the node_embeddings PostgreSQL table
- Coverage check: compare ChromaDB document count (filtered by purpose)
  against SELECT COUNT(*) FROM api_nodes WHERE status='active'

[PASTE: Phase 2 03-ui-design.md Screens 5 and 6]
```
