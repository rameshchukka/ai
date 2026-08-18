# Module 3 — Diagrams

## 1. Core RAG flow

```
  User question
       |
       v
 ┌──────────────┐
 │ (optional)    │  query rewriting / HyDE / multi-query
 │ Query transform│
 └──────┬───────┘
        v
 ┌──────────────┐      ┌─────────────────┐
 │  Embed query  │ ---> │  Vector DB       │ ---> top-k candidate chunks
 └──────────────┘      │  (+ optional     │
                        │   BM25 hybrid)   │
                        └─────────────────┘
                                |
                                v
                     ┌────────────────────┐
                     │  (optional) Rerank  │  cross-encoder or LLM
                     └────────────────────┘
                                |
                                v
                  final context chunks (small, high-precision)
                                |
                                v
                 ┌───────────────────────────┐
                 │ Generator LLM              │
                 │ prompt = question + chunks │
                 └───────────────────────────┘
                                |
                                v
                          Grounded answer
```

## 2. Chunking strategy decision tree

```
            What does the source document look like?
                            |
        ┌───────────────────┼───────────────────┐
        v                   v                   v
   Plain prose         Tables/FAQ/rows      Long-form, no
                                              clear structure
        |                   |                   |
        v                   v                   v
   Recursive split     Structural split    Semantic split
   (paragraph/sentence) (split on rows/    (split where adjacent
                         Q&A boundaries)    sentence similarity drops)

        Need both precise matching AND full context for generation?
                            |
                            v
                    Parent-child chunking
              (small chunk matches, large chunk returned)
```

## 3. Advanced retrieval techniques, where they sit in the pipeline

```
 user question: "how do u stop the loop thing"   (vague, colloquial)
       |
       v query rewriting
 "How do you implement a stopping condition in an agentic loop?"
       |
       v HyDE (alternative path)
 [LLM hallucinates a plausible answer] -> embed THAT -> search
       |
       v multi-query (alternative path)
 ["stopping condition agent loop", "agent loop termination",
  "when does a ReAct agent stop"]  -> retrieve for each -> merge
```

## 4. Evaluation: where faithfulness vs relevance diverge

```
 Question: "What is MCP?"
 Retrieved context: "RAG combines retrieval and generation."  (WRONG chunk)
 Answer: "MCP is a protocol for tool calling."  (happens to be true,
                                                  but NOT from context)

       context precision: LOW  (wrong chunk retrieved)
       faithfulness:       LOW  (answer not grounded in given context,
                                  even though it's factually correct)
       answer relevance:  HIGH  (it does answer the question asked)

 -> all three metrics disagree, which is exactly why you track them
    separately instead of one blended "quality" score.
```
