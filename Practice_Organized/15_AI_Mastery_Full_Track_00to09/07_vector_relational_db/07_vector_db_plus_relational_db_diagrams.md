# Module 7 — Diagrams

## 1. Separate-DB pattern (what you built earlier)

```
   query
     |
     v
 ┌──────────┐     top-k ids      ┌──────────────┐
 │  Chroma   │ ─────────────────> │  app code     │
 │ (vectors) │                    │  joins by id  │
 └──────────┘                    └──────┬───────┘
                                          v
                                 ┌──────────────┐
                                 │  Postgres     │
                                 │ (metadata,    │
                                 │  permissions, │
                                 │  full content) │
                                 └──────────────┘
                                          |
                                          v
                                  final filtered,
                                  enriched results
```

## 2. pgvector pattern (one system)

```
   ┌──────────────────────────────────────────┐
   │  Postgres                                  │
   │   SELECT id, content                       │
   │   FROM documents                            │
   │   WHERE owner_id = current_user             │   <- relational filter
   │   ORDER BY embedding <=> query_vector        │   <- vector similarity
   │   LIMIT 5;                                   │      same query!
   └──────────────────────────────────────────┘
```

## 3. Permission filtering: wrong vs right order

```
 WRONG (filter after retrieval):
 top-5 vector search ──> [doc_A(denied), doc_B(denied), doc_C(denied),
                            doc_D(denied), doc_E(denied)]
                              |
                              v filter by permission
                          [ ]  <- zero usable results, even though
                                  doc_F (permitted, rank 6) existed


 RIGHT (filter during retrieval):
 vector search WHERE owner_id = current_user
                              |
                              v
                    [doc_F(rank1), doc_G(rank2), ...]  <- all usable
```

## 4. Index type inside pgvector

```
                pgvector index types
                        |
            ┌───────────┴───────────┐
            v                       v
        ivfflat                   hnsw
   (needs a training/        (no training step,
    clustering step           generally better
    before first use)         accuracy/speed
                               trade-off)
```
