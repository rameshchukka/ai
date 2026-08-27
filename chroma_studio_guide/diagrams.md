# RAGAS — Diagrams

## 1. The four core metrics map onto the two halves of RAG

```
                    RAG SYSTEM
   ┌─────────────────────────┬─────────────────────────┐
   │      RETRIEVAL           │       GENERATION         │
   │  (find the chunks)       │   (write the answer)     │
   └─────────────────────────┴─────────────────────────┘
              │                          │
    ┌─────────┴─────────┐      ┌─────────┴─────────┐
    ▼                   ▼      ▼                   ▼
 Context            Context  Faithfulness      Answer
 Precision          Recall   (grounded?)       Relevancy
 (useful &          (complete?)                (on-topic?)
  ranked high?)

 "Did we fetch the           "Did the LLM use what
  right stuff?"               we fetched, correctly?"
```

## 2. What each metric actually needs as input

```
                          question  answer  retrieved_contexts  reference
                          --------  ------  ------------------  ---------
 Context Precision           ✓        ✓             ✓          (better with)
 Context Recall              ✓                      ✓              ✓ (required)
 Faithfulness                         ✓             ✓
 Answer Relevancy            ✓        ✓             ✓
 Answer Correctness          ✓        ✓                            ✓ (required)

 "reference" = a human-written ground-truth answer.
 Metrics with no ✓ in the reference column are REFERENCE-FREE — the big
 selling point of RAGAS (evaluate without labelling every example).
```

## 3. How Faithfulness is computed (the atomic-claims idea)

```
 Answer: "The refund takes 5 days and is sent by cheque."
                    │
                    ▼  LLM decomposes into atomic claims
   ┌────────────────────────────────────────────┐
   │ claim 1: refund takes 5 days                 │
   │ claim 2: refund is sent by cheque            │
   └────────────────────────────────────────────┘
                    │
                    ▼  check each claim against retrieved context
   Retrieved context says: "Refunds are processed in 5 business days
                            to the original payment method."
                    │
   claim 1: SUPPORTED ✓   (context confirms 5 days)
   claim 2: NOT SUPPORTED ✗ (context says original payment method,
                             not cheque — this is a hallucination)
                    │
                    ▼
   Faithfulness = supported / total = 1/2 = 0.50
```

## 4. Your environment: swap OpenAI for in-house models

```
 DEFAULT RAGAS (blocked in your org):
   evaluate(dataset, metrics) ──► calls OpenAI GPT + OpenAI embeddings ──► ✗ blocked

 YOUR SETUP (works):
   from ragas.llms import LangchainLLMWrapper
   from ragas.embeddings import LangchainEmbeddingsWrapper

   evaluator_llm  = LangchainLLMWrapper(get_chat_model())          # in-house chat model
   evaluator_emb  = LangchainEmbeddingsWrapper(InHouseEmbeddings()) # in-house Jina

   evaluate(dataset, metrics,
            llm=evaluator_llm,          ◄── judge is YOUR model
            embeddings=evaluator_emb)   ◄── no OpenAI, no external calls
```

## 5. The measure-improve loop RAGAS enables

```
   build/change RAG pipeline
            │
            ▼
   run RAGAS on a fixed eval set  ◄─────────┐
            │                                │
            ▼                                │
   faithfulness ↓ ?  answer_relevancy ↓ ?    │
            │                                │
            ▼                                │
   diagnose WHICH metric dropped ──► fix that specific part
            │                                │
            └────────────────────────────────┘
   (never ship a change without re-running the eval set)
```
