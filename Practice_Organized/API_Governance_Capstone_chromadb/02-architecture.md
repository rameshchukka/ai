# Architecture Guide
## Mule API Structural Detection Platform — Phase 1 (ChromaDB variant)

**Note:** Phase 1 (structural detection) does not use any vector store.
ChromaDB is installed and the client is initialised in this phase but
the collection is not yet populated. ChromaDB is activated in Phase 2.

---

## 1. Stack summary

| Concern | Choice | Deferred alternative |
|---|---|---|
| Application framework | Streamlit | — |
| Primary database | PostgreSQL 15+ | — |
| Graph traversal | PostgreSQL recursive CTE | Neo4j |
| Graph visualisation | streamlit-agraph | — |
| Vector store | ChromaDB (installed, collection created, not yet populated) | pgvector |
| LLM integration | None in this phase | Internal LLM endpoint (Phase 2) |
| API layer | None — Streamlit calls core/ directly | GraphQL / REST |
| Scheduling | APScheduler or cron | — |

---

## 2. App layer: Streamlit, not Flask/FastAPI

### Decision
Streamlit for all UI. The core/ Python modules are imported directly.
No REST or GraphQL layer between UI and database.

### Reasoning
- Internal tool for architects and developers, not a public web application
- Removing the API layer removes a whole category of milestone with no
  value for this use case
- Direct function calls are simpler to test and debug

### When to revisit
If CI/CD pipelines or external tools need to query the platform programmatically,
add a thin FastAPI wrapper around the same core/ functions at that point.

---

## 3. Graph traversal: PostgreSQL recursive CTE, not Neo4j

### Decision
All graph traversal runs as a recursive CTE inside PostgreSQL and is
materialised into the `flows` table. No graph database.

### Reasoning

| Concern | Neo4j | PostgreSQL recursive CTE |
|---|---|---|
| Infrastructure | Separate service to run, monitor, back up | Already running — zero extra ops |
| Data consistency | Two databases to keep in sync | One database — no sync problem |
| Scale | Optimised for massive graphs | Efficient up to ~50K nodes/edges |
| Query flexibility | Cypher — expressive but another language | SQL — already known |

At ~700 Mule projects and ~4,000 edges, PostgreSQL handles traversal
comfortably. Materialising flows into the `flows` table means the UI
reads pre-computed results — no traversal at query time.

### When to revisit
If node/edge count reaches ~50K or traversal time exceeds 30 seconds.

---

## 4. No API layer

### Decision
Streamlit pages import core/ modules directly. No Flask, FastAPI, or
GraphQL layer between them.

### Reasoning
Internal tool, small concurrent user base, no external API consumers
in Phase 1. Adding an API layer now is engineering for a use case that
does not yet exist.

---

## 5. Vector store: ChromaDB (installed in Phase 1, populated in Phase 2)

### Decision
ChromaDB as the vector store for semantic embeddings. The client is
installed and the persistent collection is created in Phase 1 M1, but
no embeddings are inserted until Phase 2 M3.

### Why ChromaDB

| Concern | ChromaDB | pgvector |
|---|---|---|
| Setup | `pip install chromadb` — no PostgreSQL extension needed | Requires pgvector extension compiled for your PostgreSQL version |
| Embedding API | Native `collection.add()` / `collection.query()` | Raw SQL with VECTOR type and `<=>` operator |
| Metadata filtering | Built-in metadata dict per document | Requires JOIN to relational tables |
| Persistence | `PersistentClient(path="./chroma_data")` — file-based | Inside PostgreSQL — same backup as other data |
| Operational overhead | Separate directory to back up | Included in PostgreSQL backup |
| JOIN with relational data | Requires two queries + application join | Single SQL query with JOIN |

ChromaDB is the simpler starting point when the team is comfortable
with Python but less experienced with PostgreSQL extensions. The
trade-off is that combining vector search with relational filters
requires two round-trips instead of one SQL query.

### ChromaDB setup

```python
import chromadb

# Persistent client — data survives restarts
client     = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(
    name="api_knowledge",
    metadata={"hnsw:space": "cosine"}   # cosine distance for similarity
)
```

### When to revisit
- If the team needs to combine vector similarity with complex SQL filters
  in a single query (e.g. "find semantically similar APIs in domain X that
  are active and owned by team Y") — pgvector handles this in one query,
  ChromaDB requires two round-trips
- If operational simplicity of a single database becomes important
  (pgvector keeps everything in one PostgreSQL backup)
- If vector count exceeds ~1M documents and ChromaDB performance degrades

---

## 6. No LLM in this phase

### Decision
No calls to the internal LLM endpoint in Phase 1. All detection logic is
deterministic SQL and Python.

### What this means in practice

| Feature | Phase 1 | Phase 2 |
|---|---|---|
| Duplicate flow detection | Structural graph shape only | + semantic similarity confirmation |
| Merge candidate scoring | Structural score only | + LLM rationale |
| API Discovery | Not built | Semantic + field + taxonomy search |
| Composition advisory | Not built | Full RAG pipeline with ChromaDB retrieval |

---

## 7. Project structure

```
project/
├── core/
│   ├── db.py           # PostgreSQL connection management
│   ├── traversal.py    # Recursive CTE, flow materialisation
│   ├── rules.py        # 4 structural detectors
│   └── graph.py        # networkx graph builder from DB
├── app/
│   ├── 1_Graph_Explorer.py
│   ├── 2_Findings_Dashboard.py
│   └── 3_Merge_Impact.py
├── chroma_data/        # ChromaDB persistent storage (created in Phase 2)
├── sql/
│   └── schema.sql      # All 21 DDL statements (full schema)
├── scripts/
│   ├── ingest.py       # Node + edge ingestion pipeline
│   └── refresh.py      # Weekly refresh job
└── .env
```

---

## 8. Summary table

| Decision | Alternative considered | Choice | Revisit when |
|---|---|---|---|
| App framework | Flask + React | Streamlit | External API consumers needed |
| Graph traversal | Neo4j | PostgreSQL recursive CTE | > 50K nodes/edges |
| API layer | FastAPI / GraphQL | None (direct import) | CI/CD integration needed |
| LLM integration | LLM for all scoring | None in Phase 1 | Structural findings validated |
| Vector store | pgvector | ChromaDB (installed, not yet populated) | Single-database simplicity needed |
