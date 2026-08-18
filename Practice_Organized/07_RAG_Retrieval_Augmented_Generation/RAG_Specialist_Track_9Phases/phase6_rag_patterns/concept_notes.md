# Phase 6 — RAG Patterns

## The 8 patterns
| Pattern | Core idea | Enterprise priority (per your notes) |
|---|---|---|
| Naive RAG | Retrieve top-k, stuff into prompt, generate | Baseline, always start here |
| Hybrid RAG | BM25 + vector search combined (Phase 5) | **Priority** |
| Agentic RAG | An agent decides whether/when/how to retrieve, possibly across multiple tools/sources, possibly iterating | **Priority** |
| Graph RAG | Retrieval over a knowledge graph instead of/alongside a vector store | **Priority** |
| Corrective RAG (CRAG) | Evaluate retrieved chunks' relevance; if poor, fall back to a corrective action (web search, query rewrite, broader retrieval) | Strong for high-stakes accuracy needs |
| Adaptive RAG | Route the query to different retrieval strategies based on query type/complexity (classify first, then retrieve) | Strong when query types vary widely |
| Multi-hop RAG | Answer questions requiring chaining multiple retrieval steps (retrieve, extract a sub-fact, retrieve again using that fact) | Needed for genuinely multi-step questions |
| Fusion RAG | Multiple query variations retrieved in parallel, results fused (often via RRF, Phase 5) | Overlaps heavily with multi-query + hybrid |

"Parent-child RAG" in your enterprise-priority list refers to using parent-child
chunking (Phase 2) + parent document retrieval (Phase 5) as the backbone of the
whole pipeline, rather than being an 9th distinct pattern — it's the chunking +
retrieval combination most enterprise API/documentation RAG systems converge on.

## Corrective RAG (CRAG), worked through
```
retrieve top-k
     |
     v
evaluate relevance (LLM judges: are these chunks actually relevant?)
     |
  ┌──┴──┐
 good   bad
  |      |
  v      v
generate  corrective action:
 normally  - rewrite the query and retry, or
            - fall back to a broader/different source, or
            - explicitly tell the user retrieval failed
```

## Where ChromaDB fits in this phase
Naive/Hybrid/Fusion RAG query Chroma directly (possibly multiple times). Agentic
RAG treats a Chroma query as one tool among several an agent can choose to call.
Graph RAG typically uses a graph store *alongside* Chroma — Chroma for
semantic/textual retrieval, a graph (e.g. via `networkx` for this worksheet's
scale) for relationship traversal — and a real system often merges results from
both. CRAG and Adaptive RAG wrap Chroma queries with an evaluation/routing step
before deciding what to do with the result.

## Teaser problem
> You built Agentic RAG: an agent that can call a `search_docs` tool backed by
> Chroma. On a multi-part question ("compare the auth method and rate limits of
> APIs A and B"), it calls the tool once with the whole question and gets back
> a confusing mixed bag of chunks about both APIs' auth AND limits, then writes
> a muddled answer. What's the actual problem, and which pattern fixes it?

**Solution:** the agent treated a compound question as one retrieval call. The
fix is **multi-hop RAG behavior** layered onto the agentic loop: the agent
should decompose the question into sub-queries ("auth method of API A", "rate
limits of API A", "auth method of API B", "rate limits of API B"), call
`search_docs` once per sub-query, and only then synthesize. This is exactly the
same decomposition instinct as multi-query retrieval (Phase 5), but applied at
the *reasoning* level by the agent rather than as a fixed preprocessing step.
See the worksheet's Agentic RAG section for both the naive and decomposed
versions side by side.
