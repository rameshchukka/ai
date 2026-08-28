# Phase 8 — Evaluation

## The 7 metrics
| Metric | Measures | Needs a labeled "gold" set? |
|---|---|---|
| Precision@K | Of the top-K retrieved, how many are actually relevant? | Yes (relevance labels) |
| Recall@K | Of all relevant docs in the corpus, how many appear in top-K? | Yes — and needs to know the *full* relevant set, not just what was retrieved |
| MRR (Mean Reciprocal Rank) | How high does the FIRST relevant result rank, averaged across queries? | Yes |
| NDCG (Normalized Discounted Cumulative Gain) | Like Precision@K but rewards relevant results appearing EARLIER, with graded (not just binary) relevance | Yes, ideally with graded relevance (0-3 scale, not just relevant/not) |
| Answer Faithfulness | Does the generated answer only use facts present in retrieved context? | No — LLM-as-judge, no gold set needed |
| Context Precision | Of the retrieved chunks actually used, how many were relevant? | Can be done with LLM-as-judge (no gold set) or with labels (more rigorous) |
| Context Recall | Of all relevant chunks in the corpus, how many were retrieved? | Same as Recall@K — needs to know the full relevant set, hardest to automate without labels |

## The two metric families
**Retrieval-only metrics** (Precision@K, Recall@K, MRR, NDCG) evaluate the
retriever in isolation, independent of any LLM — these are classic information
retrieval metrics, decades old, model-agnostic.

**RAG-specific metrics** (Answer Faithfulness, Context Precision, Context
Recall) evaluate the *combined* retrieval+generation system, and Context
Precision/Recall specifically can be computed either the classic IR way (with
labels) or the LLM-as-judge way (without labels) — know which one a tool/paper
means when it says "context precision," since the two computation methods can
disagree.

## MRR worked example
```
Query 1: first relevant result at rank 2  -> reciprocal rank = 1/2 = 0.5
Query 2: first relevant result at rank 1  -> reciprocal rank = 1/1 = 1.0
Query 3: first relevant result at rank 4  -> reciprocal rank = 1/4 = 0.25
MRR = mean(0.5, 1.0, 0.25) = 0.583
```

## Where ChromaDB fits in this phase
Every metric here is computed *from* Chroma query results — you run real
queries against your real collection, compare returned ids against a labeled
relevant-set (for IR metrics) or feed the returned context to an LLM judge (for
RAG-specific metrics). Chroma itself has no built-in evaluation feature; this
phase is entirely about instrumenting and scoring what Chroma gives back.

## Teaser problem
> Your Recall@5 is consistently low (0.3) across many queries, but Precision@5
> looks fine (0.8). Your first instinct is "the retriever is bad." Is that the
> right conclusion?

**Solution:** not necessarily — check how many *total* relevant documents exist
per query in your gold set first. If a query has 15 relevant documents in the
corpus and you only retrieve 5, Recall@5 is mathematically capped at 5/15 = 0.33
even with perfect precision. Low recall with high precision at small K is often
a **K-too-small** problem, not a retrieval-quality problem — try Recall@20 before
concluding the retriever itself is underperforming. See the worksheet for this
exact distinction computed on a small example.
