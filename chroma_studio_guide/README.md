# RAGAS — RAG System Evaluation (Theory + Practice)

Everything you need to evaluate a RAG system with RAGAS, the standard open-source
RAG evaluation framework — and, crucially, wired to **your in-house models** instead
of the OpenAI default (which your org blocks).

## Files
- `concept_notes.md` — theory & fundamentals: what RAGAS is, the four core metrics,
  how faithfulness is computed, the version situation, and where RAGAS fits alongside
  the classic IR metrics you already know
- `diagrams.md` — visual explanations of the metrics and the in-house-model swap
- `worksheet.ipynb` — two-part practical:
  - **Part 1** reimplements the metrics from scratch with a mock judge (runs offline
    right now — verified) so you understand the internals
  - **Part 2** uses the real `ragas` library, wired to your in-house chat + Jina
    models (needs your live endpoints)

## The one thing that matters most for your environment
RAGAS metrics are **LLM-judged** — every metric calls an LLM, and some call an
embedding model. RAGAS defaults to OpenAI. You must swap that for your in-house
models:

```python
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from inhouse_wrappers import get_chat_model, InHouseEmbeddings

evaluator_llm = LangchainLLMWrapper(get_chat_model())
evaluator_embeddings = LangchainEmbeddingsWrapper(InHouseEmbeddings())

evaluate(dataset, metrics, llm=evaluator_llm, embeddings=evaluator_embeddings)
```

No OpenAI, no external calls. Part 2 of the worksheet shows this in full.

## Install
```bash
pip install "ragas>=0.2,<0.3" datasets langchain langchain-openai
```
Pinned to the 0.2.x line because that's the most widely-documented stable API and
what the worksheet targets. (`langchain-openai` is a RAGAS dependency even though
you won't call OpenAI.) Needs Python 3.10+ — you're on 3.12.

## The four core metrics (start here)
| Metric | Grades | Reference-free? |
|---|---|---|
| Faithfulness | Is the answer grounded in retrieved context? (hallucination check) | Yes |
| Answer Relevancy | Does the answer address the question? | Yes |
| Context Precision | Is retrieved context relevant and well-ranked? | Better with reference |
| Context Recall | Did retrieval get everything needed? | Needs reference |

## How to work through it
1. Read `concept_notes.md` (the teaser at the end is the key expert insight).
2. Skim `diagrams.md`.
3. Run **Part 1** of the worksheet now — it's offline, and building the metrics from
   scratch is what makes you trust them.
4. Run **Part 2** in your environment once your in-house endpoints are reachable.

## Where this fits with your other material
- Specialist Track Phase 8 and gap-filler `02_evaluation_harness.ipynb` cover the
  classic IR metrics (Precision@K, Recall@K, MRR, NDCG) — retrieval-only, need labels.
- **RAGAS covers what those can't:** LLM-judged answer quality (faithfulness,
  relevancy) and mostly without labels, grading the *generation* half too.
- An expert uses both: IR metrics to check retrieval found the right chunks, RAGAS
  to check the whole system's answers are faithful and on-topic.

## Honesty note
Part 1 is verified to run (offline, mock judge). Part 2 uses the real library and
real LLM judge calls, which need your live endpoints — so it's written for your
environment and hasn't been executed here. The RAGAS class names are version-specific
(see the version note at the end of the worksheet); if an import fails, check
`ragas.__version__` and match names to that version's docs. The concepts don't change
across versions — only the function names do.
