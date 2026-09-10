# Software Requirements Specification
## Mule API Semantic Detection & Composition Phase — Phase 2 (ChromaDB variant)

**Prerequisite:** Phase 1 fully live and validated.
All 19 PostgreSQL tables already exist. This phase populates the reserved
tables and activates ChromaDB for vector storage.

**Key difference from pgvector variant:** Embeddings are stored in ChromaDB
(`chroma_data/` directory), not in `node_embeddings` PostgreSQL table.
The `node_embeddings` table remains empty. All relational data stays in PostgreSQL.

---

## 1. Tables activated in this phase

| Table | Phase 2 status | Populated in |
|---|---|---|
| `functionality_taxonomy` | Now populated | M3 |
| `api_fields` | Now populated | M3 |
| `api_specs` | Now populated | M3 |
| `field_mappings` | Now populated | M5 |
| `composition_candidates` | Now populated | M6 |
| `llm_call_log` | Now populated | M6b |
| `merge_candidates` | Updated | M6b (semantic_score + llm_rationale added) |
| `node_embeddings` | **Stays empty** | ChromaDB used instead |

---

## 2. Source data format extension

Same as pgvector variant — adds structured fields to Phase 1 format:

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
    {"path": "mandate_id",    "type": "string",  "required": true,
     "description": "Mandate identifier", "example": "MND-001"},
    {"path": "debit.amount",  "type": "decimal", "required": true,
     "description": "Debit amount",       "example": "5000.00"},
    {"path": "bank.ifsc_code","type": "string",  "required": true,
     "description": "Bank IFSC code",     "example": "HDFC0001234"}
  ],
  "response_fields_structured": [
    {"path": "transaction_id","type": "string",  "required": true,
     "description": "Transaction ID",     "example": "CLR-001"},
    {"path": "status",        "type": "string",  "required": true,
     "description": "SUBMITTED|FAILED",   "example": "SUBMITTED"}
  ]
}
```

---

## 3. ChromaDB setup and collection design

```python
import chromadb

# Persistent client — data stored in chroma_data/ directory
# This directory must be backed up alongside PostgreSQL
client = chromadb.PersistentClient(path="./chroma_data")

collection = client.get_or_create_collection(
    name="api_knowledge",
    metadata={"hnsw:space": "cosine"}   # cosine distance matching
)
```

### Collection schema (one document per chunk per API)

Each ChromaDB document has:
- `id` — unique string: `"{node_id}_{chunk_type}"`
- `document` — the prose text that was embedded
- `embedding` — the vector (provided explicitly when using internal LLM)
- `metadata` — dict of relational attributes for filtering

```python
{
  "id":        "142_purpose",
  "document":  "Orchestrates NACH debit - validates mandate and submits to clearance.",
  "embedding": [...],   # from internal LLM
  "metadata": {
      "node_id":       142,
      "project_name":  "proc-nach-debit-api",
      "layer":         "proc",
      "domain":        "payments",
      "domain_id":     3,
      "functionality": "NACH Debit Processing",
      "chunk_type":    "purpose",
      "status":        "active"
  }
}
```

---

## 4. Chunking strategy

| Source field(s) | Chunk type | In ChromaDB |
|---|---|---|
| `purpose_text` + `functionality` | `purpose` | Yes |
| `business_rules` (if available) | `business_rules` | Yes |
| `request_fields_structured` (as prose) | `request_fields` | Yes |
| `response_fields_structured` (as prose) | `response_fields` | Yes |

Each API produces 3-4 documents in ChromaDB.
At ~700 APIs: ~2,100-2,800 documents in the collection.

---

## 5. Ingestion — ChromaDB

```python
import chromadb

client     = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(
    name="api_knowledge",
    metadata={"hnsw:space": "cosine"}
)

def build_chunks(api_doc: dict, node_id: int) -> list[dict]:
    """Build 3-4 prose chunks per API for ChromaDB."""
    base_meta = {
        "node_id":       node_id,
        "project_name":  api_doc["project_name"],
        "layer":         api_doc["layer"],
        "domain":        api_doc.get("domain", ""),
        "functionality": api_doc.get("functionality", ""),
        "status":        "active"
    }
    chunks = [{
        "id":       f"{node_id}_purpose",
        "document": f"{api_doc.get('purpose_text','')} {api_doc.get('functionality','')}".strip(),
        "metadata": {**base_meta, "chunk_type": "purpose"}
    }]
    if api_doc.get("business_rules"):
        chunks.append({
            "id":       f"{node_id}_business_rules",
            "document": api_doc["business_rules"],
            "metadata": {**base_meta, "chunk_type": "business_rules"}
        })
    req_fields = api_doc.get("request_fields_structured", [])
    if req_fields:
        prose = " ".join(f"{f['path']} ({f['type']}) {f.get('description','')}"
                         for f in req_fields)
        chunks.append({
            "id":       f"{node_id}_request_fields",
            "document": prose,
            "metadata": {**base_meta, "chunk_type": "request_fields"}
        })
    resp_fields = api_doc.get("response_fields_structured", [])
    if resp_fields:
        prose = " ".join(f"{f['path']} ({f['type']}) {f.get('description','')}"
                         for f in resp_fields)
        chunks.append({
            "id":       f"{node_id}_response_fields",
            "document": prose,
            "metadata": {**base_meta, "chunk_type": "response_fields"}
        })
    return chunks


def ingest_to_chromadb(api_doc: dict, node_id: int, get_embedding_fn):
    """Embed each chunk and upsert into ChromaDB collection."""
    chunks = build_chunks(api_doc, node_id)
    ids, documents, embeddings, metadatas = [], [], [], []
    for c in chunks:
        if not c["document"].strip():
            continue
        ids.append(c["id"])
        documents.append(c["document"])
        embeddings.append(get_embedding_fn(c["document"]))
        metadatas.append(c["metadata"])

    if ids:
        collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
```

---

## 6. Retrieval — ChromaDB

### Use case 1: Requirement matching (composition)

```python
def search_by_requirement(requirement: str, top_k: int = 5) -> list[dict]:
    """Embed requirement and find most similar APIs in ChromaDB."""
    vec = get_embedding(requirement)
    results = collection.query(
        query_embeddings=[vec],
        n_results=top_k,
        where={"$and": [
            {"chunk_type": {"$eq": "purpose"}},
            {"status":     {"$eq": "active"}}
        ]},
        include=["documents", "metadatas", "distances"]
    )
    candidates = []
    for i in range(len(results["ids"][0])):
        distance  = results["distances"][0][i]
        meta      = results["metadatas"][0][i]
        similarity = 1 - distance              # cosine distance -> similarity
        candidates.append({
            "node_id":      meta["node_id"],
            "project_name": meta["project_name"],
            "layer":        meta["layer"],
            "domain":       meta["domain"],
            "functionality":meta["functionality"],
            "similarity":   round(similarity, 4),
            "purpose_text": results["documents"][0][i]
        })
    return candidates


def search_by_node(node_id: int, top_k: int = 10) -> list[dict]:
    """Find APIs similar in purpose to a given node (redundancy check)."""
    # Get this node's purpose embedding from ChromaDB
    existing = collection.get(
        ids=[f"{node_id}_purpose"],
        include=["embeddings"]
    )
    if not existing["embeddings"]:
        return []
    source_vec = existing["embeddings"][0]

    results = collection.query(
        query_embeddings=[source_vec],
        n_results=top_k + 1,       # +1 because the node itself will appear
        where={"$and": [
            {"chunk_type": {"$eq": "purpose"}},
            {"status":     {"$eq": "active"}},
            {"node_id":    {"$ne": node_id}}   # exclude self
        ]},
        include=["metadatas", "distances"]
    )
    candidates = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        candidates.append({
            "node_id":      meta["node_id"],
            "project_name": meta["project_name"],
            "layer":        meta["layer"],
            "domain":       meta["domain"],
            "similarity":   round(1 - results["distances"][0][i], 4)
        })
    return candidates


def search_by_field_change(change_description: str, top_k: int = 10) -> list[dict]:
    """Find APIs referencing similar field concepts (change impact)."""
    vec = get_embedding(change_description)
    results = collection.query(
        query_embeddings=[vec],
        n_results=top_k,
        where={"$and": [
            {"chunk_type": {"$in": ["request_fields", "response_fields"]}},
            {"status":     {"$eq": "active"}}
        ]},
        include=["metadatas", "distances"]
    )
    seen = set()
    candidates = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        nid  = meta["node_id"]
        if nid not in seen:
            seen.add(nid)
            candidates.append({
                "node_id":      nid,
                "project_name": meta["project_name"],
                "chunk_type":   meta["chunk_type"],
                "similarity":   round(1 - results["distances"][0][i], 4)
            })
    return candidates
```

---

## 7. Composition validator

Identical to pgvector variant except retrieval uses ChromaDB.
See Phase 2 pgvector SRS Sections 6.1-6.3 for scoring formulas.

---

## 8. LLM integration points (4 total)

Identical to pgvector variant.
All LLM calls log to `llm_call_log` PostgreSQL table.
See `07-llm-integration-guide.md` for full prompt text.

---

## 9. ChromaDB vs pgvector — the key operational difference

```
ChromaDB retrieval for composition:
  Step 1: collection.query(query_embeddings=[vec], where={"chunk_type":"purpose"})
          -> returns top-K node_ids and similarity scores
  Step 2: SELECT n.* FROM api_nodes n WHERE n.node_id IN (returned_ids)
          -> separate SQL query to get relational fields
  Step 3: Application joins the two result sets

pgvector retrieval for composition:
  Step 1: One SQL query with JOIN:
          SELECT n.*, 1-(e.embedding <=> vec) AS sim
          FROM node_embeddings e JOIN api_nodes n ON n.node_id=e.node_id
          WHERE e.chunk_type='purpose' AND n.status='active'
          ORDER BY e.embedding <=> vec LIMIT 5
  Done.
```

This two-step pattern is abstracted into `core/vector_store.py` so the
Streamlit pages and composition logic are identical between ChromaDB and
pgvector variants.

---

## 10. Open decisions

- `DIRECT_MATCH_THRESHOLD = 0.85` — tune after first labelled test set
- `COMPOSE_THRESHOLD = 0.60` — tune after architect review
- Composition formula weights (0.40/0.35/0.25) — tune after first 20 reviews
- ChromaDB `chroma_data/` directory must be included in backup procedures
