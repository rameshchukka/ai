# Phase 5 — Diagrams

## 1. All techniques as wrappers around the same Chroma primitive

```
                    collection.query(embedding, where=..., n_results=...)
                                  |
        ┌──────────────┬──────────┼──────────┬──────────────┐
        v              v          v          v              v
  Similarity      Metadata    Multi-query  Self-query   Parent doc
  search           filter     (call query   (LLM builds  (call query,
  (call as-is)    (add `where`  N times,    the `where`   then look up
                   dict)         merge)      dict, THEN    parent_id of
                                              call query)   the winning
                                                            chunk)
```

## 2. Reciprocal Rank Fusion (this phase's teaser problem, solved)

```
 BM25 results (by rank):        Vector results (by rank):
 1. doc_C                       1. doc_A
 2. doc_A                       2. doc_D
 3. doc_B                       3. doc_C

 RRF score(doc) = sum over methods of  1 / (rank_in_that_method + k)   (k=60 typical)

 doc_A: 1/(2+60) + 1/(1+60) = 0.0161 + 0.0164 = 0.0325
 doc_C: 1/(1+60) + 1/(3+60) = 0.0164 + 0.0159 = 0.0323
 doc_B: 1/(3+60) + 0                = 0.0159
 doc_D: 0         + 1/(2+60)        = 0.0161

 Final fused ranking: doc_A, doc_C, doc_D, doc_B
 (ranks combine meaningfully; raw BM25 scores vs cosine scores do not)
```

## 3. Re-ranking funnel

```
  50 candidates (cheap, approximate retrieval)
        |
        v
  ┌─────────────────────┐
  │  Reranker (cross-     │   slower, more accurate,
  │  encoder or LLM)       │   only feasible on a SMALL set
  └─────────────────────┘
        |
        v
  top 5 (sent to the generator LLM)
```

## 4. Contextual compression vs parent document retrieval (easy to confuse)

```
 PARENT DOCUMENT RETRIEVAL:
   match small child -> return the WHOLE larger parent, unmodified

 CONTEXTUAL COMPRESSION:
   match/retrieve a large document -> use an LLM to EXTRACT only the
   relevant sentences/passages from within it -> return the compressed result

 Difference: parent doc retrieval returns MORE text (the full parent).
             Contextual compression returns LESS text (a distilled extract).
             They solve opposite problems: parent doc retrieval adds context
             back; compression removes irrelevant context.
```
