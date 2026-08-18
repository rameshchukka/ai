# Module 4 — Diagrams

## 1. Runnable composition (LCEL)

```
  RunnableA  |  RunnableB  |  RunnableC
  ────────────────────────────────────
  PromptTemplate  |  ChatModel  |  OutputParser
        |                |              |
        v                v              v
   fills {vars}     generates text   parses to dict/str/object
        |________________|______________|
                          |
                   single .invoke(input)
                   single .stream(input)   <- works on the WHOLE pipeline
                   single .batch(inputs)      because every piece implements
                                               the same Runnable interface
```

## 2. RunnableParallel — branching

```
                    ┌──> retriever ──> context
   question ────────┤
                    └──> RunnablePassthrough ──> original question
                              |
                              v
                    {"context": ..., "question": ...}
                              |
                              v
                       prompt | llm | parser
```

## 3. Chain (legacy) vs LCEL, structurally

```
 LEGACY CHAIN                          LCEL
 ─────────────                        ────
 RetrievalQA(                         retriever | prompt | llm | parser
   llm=...,                                |larger, but every
   retriever=...,                          |piece independently
   chain_type="stuff"                      |swappable/testable/
 )                                         |streamable
   |
   single opaque .invoke()
   internals hidden inside the class
```

## 4. LangGraph: state machine for agents

```
        ┌─────────────┐
        │  START       │
        └──────┬───────┘
               v
        ┌─────────────┐
   ┌───>│  Agent node  │  (decide: tool call or final answer?)
   │    └──────┬───────┘
   │           v
   │    ┌─────────────┐
   │    │ conditional   │── final answer ──> END
   │    │ edge          │
   │    └──────┬───────┘
   │           | tool call
   │           v
   │    ┌─────────────┐
   └────┤  Tool node   │  (execute, update shared State)
        └─────────────┘

  Shared `State` object flows through every node — this is what lets
  LangGraph express loops and multi-step memory that a linear LCEL
  pipeline can't.
```
