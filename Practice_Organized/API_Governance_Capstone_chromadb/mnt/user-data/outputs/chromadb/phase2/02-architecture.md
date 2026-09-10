# Architecture Guide — Phase 2 (ChromaDB variant)
## Mule API Semantic Detection & Composition Phase

**Changes from Phase 1:** ChromaDB collection now populated, internal LLM
wired, 3 new screens added.

---

## 1. What changes vs Phase 1

| Concern | Phase 1 | Phase 2 |
|---|---|---|
| Vector store | ChromaDB installed, collection empty | ChromaDB populated (~2,100-2,800 documents) |
| LLM | None | Internal endpoint, 4 integration points |
| Screens | 3 | 6 (add API Discovery, Composition Advisor, Embedding Health) |
| Field data | Not ingested | `api_fields` populated from structured extraction |

Everything else is unchanged — same PostgreSQL instance, same Streamlit
framework, same core/ package extended with new modules.

---

## 2. ChromaDB: why a separate vector store

ChromaDB is the vector store choice for teams that prefer:
- A Python-native API (`collection.add()`, `collection.query()`)
  over SQL with vector operators (`<=>`)
- No PostgreSQL extension compilation required
- Simpler local development setup

**The operational trade-off:**
ChromaDB is a second service/directory to operate, back up, and keep in
sync with PostgreSQL. Queries that need both vector similarity AND
relational filtering require two round-trips and an application-layer
join. The `core/vector_store.py` module abstracts this so all other code
is unaffected.

---

## 3. LLM: 4 integration points

```
Developer types requirement
        |
        v
[LLM P1] Query Expansion  -- expand to 3 semantic variants
        |
        v
[ChromaDB] collection.query()  -- cosine search on purpose chunks
        |
        v
[PostgreSQL] JOIN api_nodes  -- get relational fields for returned node_ids
        |
        v
[PostgreSQL] field_mappings lookup  -- schema compatibility (deterministic)
[LLM P2] Field Equivalence  -- only for 0.50-0.79 fuzzy matches
        |
        v
[Python] Composite score formula
[LLM P3] Composition decision  -- reads scores, decides band
        |
        v
Result rendered
[LLM P4] Discovery quick-take  -- async YES/PARTIAL/NO badge
```

---

## 4. Extended project structure

```
project/
├── core/
│   ├── db.py               # PostgreSQL connection
│   ├── graph.py            # networkx graph builder
│   ├── traversal.py        # recursive CTE
│   ├── rules.py            # 4 structural detectors
│   ├── vector_store.py     # ChromaDB client, ingest, retrieval
│   ├── composition.py      # field mapping, scoring, analyze_requirement
│   ├── search.py           # 3-mode API Discovery search
│   └── llm.py              # 4 LLM points + llm_call_log
├── app/
│   ├── 1_Graph_Explorer.py       # unchanged
│   ├── 2_Findings_Dashboard.py   # unchanged
│   ├── 3_Merge_Impact.py         # updated: llm_rationale now visible
│   ├── 4_API_Discovery.py        # NEW
│   ├── 5_Composition_Advisor.py  # NEW
│   └── 6_Embedding_Health.py     # NEW
├── chroma_data/                  # ChromaDB persistent storage
│   └── (managed by ChromaDB)
├── scripts/
│   ├── ingest.py                 # extended: adds fields + ChromaDB
│   └── refresh.py                # unchanged
└── .env
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
CHROMA_PATH=./chroma_data
CHROMA_COLLECTION=api_knowledge
```

---

## 6. `core/vector_store.py` — ChromaDB abstraction

```python
import chromadb
import os

_client     = None
_collection = None

def get_collection():
    global _client, _collection
    if _collection is None:
        path = os.getenv("CHROMA_PATH", "./chroma_data")
        name = os.getenv("CHROMA_COLLECTION", "api_knowledge")
        _client     = chromadb.PersistentClient(path=path)
        _collection = _client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )
    return _collection


def search_purpose(query_vec: list[float], top_k: int = 5,
                   domain: str = None) -> list[dict]:
    """Search ChromaDB for APIs similar to query_vec.
    Optionally filter by domain metadata."""
    coll  = get_collection()
    where = {"chunk_type": {"$eq": "purpose"}, "status": {"$eq": "active"}}
    if domain:
        where["domain"] = {"$eq": domain}

    results = coll.query(
        query_embeddings=[query_vec],
        n_results=top_k,
        where={"$and": [{k: v} for k, v in where.items()]},
        include=["documents", "metadatas", "distances"]
    )
    candidates = []
    for i, doc_id in enumerate(results["ids"][0]):
        meta = results["metadatas"][0][i]
        candidates.append({
            "node_id":      meta["node_id"],
            "project_name": meta["project_name"],
            "layer":        meta["layer"],
            "domain":       meta["domain"],
            "functionality":meta.get("functionality", ""),
            "purpose_text": results["documents"][0][i],
            "similarity":   round(1 - results["distances"][0][i], 4)
        })
    return candidates


def upsert_chunks(chunks: list[dict]):
    """Upsert a list of {id, document, embedding, metadata} dicts."""
    coll = get_collection()
    coll.upsert(
        ids        =[c["id"]        for c in chunks],
        documents  =[c["document"]  for c in chunks],
        embeddings =[c["embedding"] for c in chunks],
        metadatas  =[c["metadata"]  for c in chunks]
    )


def get_collection_count() -> int:
    return get_collection().count()
```

---

## 7. Embedding Health — ChromaDB adaptation

The Embedding Health screen queries ChromaDB for embeddings, not
`node_embeddings` PostgreSQL table. The UMAP computation and gap metric
are identical.

```python
# app/6_Embedding_Health.py — ChromaDB version
from core.vector_store import get_collection

coll = get_collection()
results = coll.get(
    where={"$and": [
        {"chunk_type": {"$eq": chunk_type}},
        {"status":     {"$eq": "active"}}
    ]},
    include=["embeddings", "metadatas"]
)
embeddings = results["embeddings"]
domains    = [m["domain"] for m in results["metadatas"]]
```

---

## 8. Summary table

| Decision | Phase 1 | Phase 2 change |
|---|---|---|
| Vector store | ChromaDB installed, empty | ChromaDB populated, HNSW index built automatically |
| LLM | None | 4 integration points, all calls logged to PostgreSQL llm_call_log |
| Field data | Not ingested | api_fields populated in PostgreSQL |
| Screens | 3 | +3 more (API Discovery, Composition Advisor, Embedding Health) |
| Merge candidates | Structural score only | + semantic score + LLM rationale |
| Backup | PostgreSQL only | PostgreSQL + chroma_data/ directory |
