# Phase 5 — Retrieval Techniques

(Numbering matches your source document, which has no Phase 4.)

## The 9 techniques
| Technique | What it does | Use when |
|---|---|---|
| Similarity search | Plain vector nearest-neighbor | Baseline — always your starting point |
| Metadata filtering | Narrow candidates by structured fields before/alongside similarity | You have structured attributes (service, environment, version) worth constraining on |
| Hybrid search | Combine BM25 (keyword) + vector (semantic) rankings | Corpus has exact-match-sensitive terms (error codes, API names) alongside natural language |
| Multi-query retrieval | Generate several rephrasings of the query, retrieve for each, merge | Vague queries, or queries whose vocabulary may not match the corpus's phrasing |
| Self-query retrieval | LLM extracts structured filters from a natural-language query automatically | You want metadata filtering (above) without making the user write filter syntax |
| Parent document retrieval | Match on a small chunk, return its larger parent for context | Same scenario as parent-child chunking (Phase 2) — precision matching, context-rich return |
| Contextual compression | Retrieve a large document, then keep only the parts relevant to the question | Large source documents where most content per-document is irrelevant to most questions |
| Re-ranking | Retrieve top-50 cheaply, rank with a stronger model, keep top-5 | Initial retrieval is noisy-but-cheap and you can afford a slower precise second pass |
| Ensemble retrieval | Combine multiple retrieval methods (BM25 + vector + metadata) and merge/vote | You want the combined strengths of several methods rather than picking one |
| Query transformation | Rewrite vague questions into more searchable ones | Same motivation as multi-query, but a single rewritten query rather than several |

## Self-query retrieval, the example from your notes, worked through
```
User: "Show failed payment APIs in production"
LLM extracts:
  service = "Payment"
  status = "Failed"
  environment = "Production"
-> these become a Chroma `where` filter, combined with whatever
   semantic component remains in the query (if any)
```
This needs the LLM to know your **metadata schema** in advance (what fields
exist, what values are valid) — usually via a short schema description in the
system prompt, similar to how you'd describe a function/tool schema.

## Where ChromaDB fits in this phase
Every technique above is implemented as a *combination* of Chroma's `query()`
(with or without `where` filters) and pre/post-processing around it — Chroma
itself only natively does similarity search + metadata filtering; everything
else (hybrid fusion, multi-query merging, reranking, self-query extraction) is
logic you write around Chroma calls, not a Chroma feature itself. The worksheet
makes this explicit by building each technique as a thin wrapper function around
plain `collection.query()` calls.

## Teaser problem
> You implement hybrid search by running BM25 and vector search separately,
> then just concatenating both result lists and taking the top 5. Results look
> worse than vector search alone. What's wrong?

**Solution:** naive concatenation doesn't account for the fact that BM25 scores
and cosine-similarity scores live on completely different scales — sorting a
concatenated list by "score" compares numbers that don't mean the same thing.
The standard fix is **Reciprocal Rank Fusion (RRF)**: convert each method's
results to *ranks* (1st place, 2nd place, ...) instead of raw scores, then
combine by summing `1/(rank + k)` across methods. Ranks are comparable across
methods even when raw scores aren't. See the worksheet's hybrid search section
for RRF implemented from scratch.
