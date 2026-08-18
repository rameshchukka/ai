# Phase 9 — Enterprise Pipelines

## The 5 pipelines
| Pipeline | Source | What's specific to this source |
|---|---|---|
| PDF → ChromaDB | PDF files | Phase 1 extraction + table-aware chunking for any embedded tables |
| Swagger → ChromaDB | OpenAPI/Swagger specs | Structure-aware chunking, one chunk per endpoint (Phase 2) |
| Database → ChromaDB | A relational DB (e.g. Postgres) | Row-based extraction; decide chunk granularity per row vs. per logical record group |
| Wiki → ChromaDB | Confluence/wiki pages (often HTML or Markdown export) | Heading-based recursive/semantic chunking; watch for stale/duplicate pages |
| Logs → ChromaDB | Application/system logs | Sliding window chunking (Phase 2) — logs are sequential/temporal, not document-structured |

## The pipeline shape every one of these shares
```
source -> extract (Phase 1) -> chunk (Phase 2, source-appropriate strategy)
       -> embed (Phase 3, in-house Jina by default)
       -> store in Chroma with metadata (source type, source id, timestamp,
                                          section/endpoint/table name)
       -> (ongoing) re-sync on source changes
```

## The part beginners skip: re-sync / freshness
A one-time ingestion script is the easy 80%. The harder, more enterprise-relevant
20% is: what happens when the source PDF gets replaced, the wiki page gets
edited, or a new log file rotates in? You need:
- A stable id scheme so re-ingesting an updated source **updates** existing
  Chroma entries (`collection.upsert()`) rather than duplicating them
- A way to detect "this source changed" (checksum, last-modified timestamp,
  version field) without re-embedding everything every time
- A deletion path for content that's been removed at the source — orphaned
  Chroma entries pointing at deleted source content are a quiet, common
  production bug

## Database → ChromaDB, a specific design decision
Unlike the other 4 sources, a relational DB already has clean structure —
the temptation is to chunk row-by-row, but the right granularity depends on
the table: a `payments` table's individual rows might each be a chunk (one
transaction = one retrievable fact), while a `services` table with a handful
of rows and rich text description columns might want each row's *description*
column treated as its own chunk, with the structured columns kept as metadata
rather than embedded text.

## Teaser problem
> Your wiki → ChromaDB pipeline ran once successfully. Three weeks later, a
> wiki page got edited to fix an outdated API version number. Your RAG system
> still confidently cites the old, wrong version number. What's missing from
> the pipeline, and what's the minimal fix?

**Solution:** there's no re-sync step — the pipeline only knows how to ingest
once. Minimal fix: store each chunk's id deterministically from its source
(e.g. `wiki_page_id + chunk_index`), and re-run ingestion periodically (or
on a webhook from the wiki) using `collection.upsert()` instead of `add()` —
upsert overwrites existing ids with new content instead of erroring or
duplicating. This doesn't require detecting *which* pages changed (though
that's a worthwhile later optimization via last-modified timestamps) — just
re-running upsert on everything is a correct, if not maximally efficient,
starting fix. See the worksheet's pipeline section for upsert implemented.
