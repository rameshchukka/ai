# Phase 6 — Diagrams

## 1. Pattern complexity ladder

```
  Naive RAG
     |
     v  (+ keyword search)
  Hybrid RAG
     |
     v  (+ relevance check + fallback)
  Corrective RAG
     |
     v  (+ query-type routing)
  Adaptive RAG
     |
     v  (+ multi-step decomposition)
  Multi-hop RAG
     |
     v  (+ agent decides retrieval strategy/timing itself)
  Agentic RAG
     |
     v  (+ relationship/graph traversal alongside vector search)
  Graph RAG

  Each rung adds one capability on top of the previous rung's complexity —
  don't reach for Agentic/Graph RAG before Naive/Hybrid RAG is solid; most
  of the value comes from the bottom of the ladder.
```

## 2. Agentic RAG: tool, not a fixed step

```
            User question
                  |
                  v
          ┌──────────────┐
          │   Agent        │  decides: do I need to search? which tool?
          └──────┬────────┘  how many times? (Module 5 of AI Mastery track)
                  |
        ┌─────────┼─────────┐
        v         v         v
   search_docs  calculator  web_search
   (Chroma)      tool        tool
        |
        v
     observation fed back to agent, loop continues until final answer
```

## 3. Multi-hop decomposition (this phase's teaser, solved)

```
 Compound question:
 "Compare the auth method and rate limits of APIs A and B"
              |
              v  decompose
 ┌─────────────────────────────────────────────┐
 │ sub-query 1: "auth method of API A"           │ -> search_docs -> chunk
 │ sub-query 2: "rate limits of API A"           │ -> search_docs -> chunk
 │ sub-query 3: "auth method of API B"           │ -> search_docs -> chunk
 │ sub-query 4: "rate limits of API B"           │ -> search_docs -> chunk
 └─────────────────────────────────────────────┘
              |
              v
   all 4 chunks given to generator together -> coherent comparison
```

## 4. Graph RAG alongside Chroma

```
              User question
                    |
         ┌──────────┴──────────┐
         v                      v
   Chroma (vector)        Graph store (networkx)
   semantic similarity    relationship traversal
   "find docs ABOUT       "find what's CONNECTED TO
    payment errors"        the Payment service"
         |                      |
         └──────────┬───────────┘
                     v
          merged context -> generator
```
