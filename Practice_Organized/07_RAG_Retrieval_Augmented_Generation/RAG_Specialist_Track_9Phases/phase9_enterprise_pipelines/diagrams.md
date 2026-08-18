# Phase 9 — Diagrams

## 1. The shared pipeline shape, all 5 sources

```
  PDF ────┐
  Swagger ─┤
  Database ┼──> extract ──> chunk (source-appropriate) ──> embed ──> Chroma
  Wiki ────┤      (Phase 1)      (Phase 2)                 (Phase 3)   |
  Logs ────┘                                                            v
                                                                  + metadata:
                                                                  source_type,
                                                                  source_id,
                                                                  timestamp,
                                                                  section/endpoint
```

## 2. The missing piece beginners skip: re-sync

```
  ONE-TIME INGESTION (the easy 80%):
  source --> extract --> chunk --> embed --> collection.add()
  Works great... once.

  PRODUCTION PIPELINE (the harder 20%):
                    ┌─────────────────────────┐
                    │  source changes detected  │  (webhook, cron diff,
                    │  (page edited, new log     │   checksum compare)
                    │   file, row updated)        │
                    └────────────┬────────────┘
                                 v
                    re-extract -> re-chunk -> re-embed
                    -> collection.upsert(id=deterministic_id, ...)
                                 |
                    same id as before? -> OVERWRITES old content
                    (this is what add() does NOT do safely)
```

## 3. Database → Chroma granularity decision

```
  payments table (many rows, short structured data)
        |
        v
  one row = one chunk        <-- "Transaction #4521: $50.00, status=completed"
                                  (structured columns become the embedded text directly)

  services table (few rows, rich free-text description column)
        |
        v
  embed the DESCRIPTION column as the chunk text
  keep other columns (owner, version, status) as METADATA, not embedded text
  --------------------------------------------------------------
  same source type (a DB table), different chunking decision per table,
  driven by what's actually meaningful to retrieve on
```

## 4. Orphaned entries — the quiet bug

```
  Day 1: wiki page "Auth Guide" ingested -> chunk ids auth_guide_0, auth_guide_1
  Day 30: wiki page "Auth Guide" DELETED from the wiki entirely
  Day 31: pipeline re-runs upsert on all CURRENT wiki pages
          ("Auth Guide" isn't in that list anymore, since it's deleted)
                    |
                    v
  auth_guide_0 and auth_guide_1 are STILL in Chroma — upsert never
  touches ids that aren't in the current batch. Without an explicit
  deletion step (diff old id list vs new id list, delete the difference),
  deleted source content keeps getting retrieved forever.
```
