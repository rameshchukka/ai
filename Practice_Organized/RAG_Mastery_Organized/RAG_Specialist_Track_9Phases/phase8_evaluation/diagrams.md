# Phase 8 — Diagrams

## 1. Metric family tree

```
                    RAG Evaluation Metrics
                            |
        ┌───────────────────┼───────────────────┐
        v                                       v
  Retrieval-only                          RAG-specific
  (classic IR, needs labels)              (LLM-as-judge OR labels)
        |                                       |
   ┌────┼────┬────────┐                  ┌──────┼──────┐
   v    v    v        v                  v             v
 P@K  R@K  MRR      NDCG          Answer Faithfulness  Context
                                                        Precision/Recall
```

## 2. Precision@K vs Recall@K, visualized

```
  Corpus has 15 relevant docs for this query (gold set known)
  Top-5 retrieved: [relevant, relevant, irrelevant, relevant, irrelevant]

  Precision@5 = relevant_in_top5 / 5        = 3/5  = 0.60
  Recall@5    = relevant_in_top5 / total_relevant = 3/15 = 0.20

  Same retrieval result, very different stories:
  "60% of what I showed you was relevant" (precision)
  "I only surfaced 20% of everything relevant that exists" (recall)
```

## 3. K-too-small problem (this phase's teaser, solved)

```
  total relevant docs for this query = 15

  Recall@5  ceiling = 5/15  = 0.33   (even with PERFECT precision)
  Recall@10 ceiling = 10/15 = 0.67
  Recall@20 ceiling = 15/15 = 1.00   (K finally large enough to capture all)

  Low Recall@5 + high Precision@5 -> check the ceiling math BEFORE
  concluding the retriever itself is bad
```

## 4. NDCG: rewards EARLY relevant results more than late ones

```
  Ranking A: [relevant, irrelevant, irrelevant, irrelevant, irrelevant]
  Ranking B: [irrelevant, irrelevant, irrelevant, irrelevant, relevant]

  Precision@5 is IDENTICAL for both (1/5 = 0.20)
  NDCG is HIGHER for Ranking A — the relevant result appearing at
  position 1 contributes more "gain" (discounted less) than the same
  relevant result buried at position 5
```
