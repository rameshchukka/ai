# Module 7 — Vector DB + Relational DB in Practice

## 1. Why combine them at all (recap + deeper dive)
Vector DBs answer "what's similar to this?" Relational DBs answer "give me
exact rows matching these conditions, with joins/transactions/constraints."
A real RAG/agent system almost always needs both: similarity search to find
candidates, then relational logic for permissions, versioning, audit trails,
and anything involving structured joins across entities.

## 2. Chroma deep dive
- **Collections**: named groups of (id, embedding, document, metadata) tuples.
- **Distance metric**: configurable per collection (cosine, l2, ip) — set this
  explicitly rather than relying on the default if you care about correctness.
- **Metadata filtering**: `where={"owner": "team_a"}` style filters combined
  with vector search — filter narrows the candidate set, vector search ranks it.
- **Persistence**: `PersistentClient` (embedded, local) vs running `chroma run`
  as a server (`HttpClient`) — you've now used both.

## 3. pgvector deep dive
- Adds a `vector` column type to Postgres; `<->` (L2), `<#>` (negative inner
  product), `<=>` (cosine distance) operators do similarity search *inside SQL*.
- Index types: `ivfflat` (older, needs a training step) vs `hnsw` (newer,
  generally better accuracy/speed trade-off, no training step needed).
- Because it's "just a column," you get full SQL: joins, transactions, row-level
  security, foreign keys — all the relational guarantees Chroma doesn't offer.

## 4. Combining patterns
| Pattern | How | Trade-off |
|---|---|---|
| Separate DBs, joined in app code | Chroma for vectors, Postgres for metadata, join by shared id (what you built earlier) | Two systems to run/backup; max flexibility per system |
| Single DB with pgvector | Everything in Postgres, vector column + relational columns together | One system, ACID guarantees across vector+relational data; less specialized vector-search tuning than dedicated vector DBs |

## 5. Decision guide
- **Small-medium corpus, want simplicity & transactional consistency** → pgvector.
- **Large-scale, need vector-DB-specific tuning (HNSW params, sharding) or
  the vector and relational data are owned by different services anyway** →
  separate Chroma/Milvus/Pinecone + Postgres, joined in app code.

## Teaser problem
> Your capstone demo needs to answer "find documents similar to X, but only
> ones the current user is permitted to see." Where should the permission
> check happen — in the vector DB's metadata filter, or after retrieval in
> the app layer?

**Solution:** prefer pushing it into the **vector DB's metadata filter** (or
the relational join, if using pgvector/separate-DB pattern) rather than
filtering top-k results in app code after retrieval. If you filter after,
you risk a top-k of 5 that's *entirely* permission-denied, returning zero
usable results even though relevant permitted documents exist further down
the ranking. See the worksheet notebook in this folder for both versions side by side.
