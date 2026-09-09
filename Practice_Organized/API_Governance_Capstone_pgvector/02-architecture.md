# Architecture Guide
## Mule API Structural Detection Platform — Phase 1

---

## 1. Stack summary

| Concern | Choice | Deferred alternative |
|---|---|---|
| Application framework | Streamlit | — |
| Primary database | PostgreSQL 15+ | — |
| Graph traversal | PostgreSQL recursive CTE | Neo4j |
| Graph visualisation | streamlit-agraph | — |
| Vector store | pgvector (extension installed, table created, not yet populated) | — |
| LLM integration | None in this phase | Internal LLM endpoint (next phase) |
| API layer | None — Streamlit calls core/ directly | GraphQL / REST |
| Scheduling | APScheduler or cron | — |

---

## 2. App layer: Streamlit, not Flask/FastAPI

### Decision
Streamlit for all UI. The core/ Python modules are imported directly — no
REST or GraphQL layer between the UI and the database.

### Reasoning
- Architects and developers, not end consumers, are the users — interactive
  data tool, not a public web application
- Removing the API layer removes one whole category of milestone (API design,
  serialisation, authentication, versioning) that adds no value for this use case
- Direct function calls are easier to test and debug than HTTP round-trips

### When to revisit
If the platform needs to be accessed by CI/CD pipelines or external tools
(e.g. a pre-merge hook that checks for redundancy), a thin REST layer becomes
worthwhile. Add it then, not now.

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
| Query flexibility | Cypher — expressive but another language to maintain | SQL — already known |
| Cold start | Schema migration, driver, connection pool | None — it is already there |

At ~700 Mule projects and ~2,000–4,000 edges, PostgreSQL handles the traversal
comfortably. Materialising flows into the `flows` table means the UI reads
pre-computed results — no traversal at query time.

### When to revisit
If node/edge count reaches ~50K or traversal time exceeds 30 seconds on a
full rebuild. Not expected at current project scale.

---

## 4. No API layer

### Decision
Streamlit pages import `core/` modules directly. No Flask, FastAPI, or
GraphQL between them.

### Reasoning
- Every abstraction layer that is not needed now is a layer to maintain forever
- The platform is an internal tool accessed by a small number of architects
  and developers — a REST API would be engineering for a use case that does not
  yet exist
- If CI/CD integration becomes a requirement later, a thin FastAPI wrapper
  around the same `core/` functions can be added without touching any existing code

---

## 5. No LLM in this phase

### Decision
No calls to the internal LLM endpoint in Phase 1. All detection logic is
deterministic SQL and Python.

### What this means in practice

| Feature | Phase 1 | Next phase |
|---|---|---|
| Duplicate flow detection | Structural graph shape only | + semantic similarity confirmation |
| Merge candidate scoring | Structural score only | + LLM rationale |
| API Discovery | Not built | Semantic + field + taxonomy search |
| Composition advisory | Not built | Full RAG pipeline |

### Why this is the right decision now
- The four structural rules are fully deterministic — graph shape does not
  need an LLM to detect a duplicate flow or a pass-through hop
- Getting real findings in front of architects now, without LLM latency and
  cost, validates that the graph extraction is correct before adding more layers
- The schema already has `llm_call_log`, `node_embeddings`, `api_specs`, etc.
  created — adding the LLM layer later requires no migration

---

## 6. Project structure

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
├── sql/
│   └── schema.sql      # All 21 DDL statements (full schema)
├── scripts/
│   ├── ingest.py       # Node + edge ingestion pipeline
│   └── refresh.py      # Weekly refresh job
└── .env
```

---

## 7. Summary table

| Decision | Alternative considered | Choice | Revisit when |
|---|---|---|---|
| App framework | Flask + React | Streamlit | External API consumers needed |
| Graph traversal | Neo4j | PostgreSQL recursive CTE | > 50K nodes/edges |
| API layer | FastAPI / GraphQL | None (direct import) | CI/CD integration needed |
| LLM integration | LLM for all scoring | None in Phase 1 | Structural findings validated |
| Vector store | Separate ChromaDB | pgvector (reserved, not yet populated) | Semantic phase begins |
