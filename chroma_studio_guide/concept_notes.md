# RAGAS — Concept Notes (Theory & Fundamentals)

RAGAS (Retrieval-Augmented Generation Assessment) is the most widely-used
open-source framework for evaluating RAG systems. Where your Specialist Track
Phase 8 taught you to compute Precision@K / Recall@K / MRR / NDCG by hand,
RAGAS automates a *different and complementary* set of metrics — ones that need
an LLM to judge, and that mostly **don't require a labelled ground-truth set**.

## Why RAGAS exists (the core idea)
Classic IR metrics (precision/recall) need you to know, in advance, which
documents are "relevant" for each query — a labelled gold set. That's expensive
to build. RAGAS's insight: use a capable LLM *as the judge* to score qualities
like "is this answer actually grounded in the retrieved context?" without a human
having to label every example first. This turns "ship and pray" into a
"measure and improve" loop.

## The evaluation is LLM-based — this matters for your setup
Every RAGAS metric is powered by an LLM (the "evaluator" or "judge" LLM), and a
few also need an embedding model. **By default RAGAS uses OpenAI**, but it wraps
any LangChain-compatible LLM/embeddings. In your environment (OpenAI blocked,
in-house models only) you **must** point RAGAS at your in-house models via
`LangchainLLMWrapper` and `LangchainEmbeddingsWrapper`. The worksheet shows
exactly this — it's the single most important setup step for you.

## The four core metrics (the classic "Ragas score")
These four are the foundation. Two evaluate **retrieval**, two evaluate
**generation** — mapping neatly onto the two halves of a RAG system.

| Metric | Half of RAG it grades | Question it answers | Needs ground truth? |
|---|---|---|---|
| **Context Precision** | Retrieval | Of the retrieved chunks, how many are actually relevant, and are the relevant ones ranked high? | No (uses the answer) / better with it |
| **Context Recall** | Retrieval | Did retrieval fetch *all* the context needed to answer? | **Yes** — needs a reference answer |
| **Faithfulness** | Generation | Is every claim in the answer supported by the retrieved context (no hallucination)? | No |
| **Answer Relevancy** | Generation | Does the answer actually address the question (not evasive/padded)? | No |

### Faithfulness — the most important one for production
Faithfulness decomposes the generated answer into individual atomic claims, then
checks each claim against the retrieved context. Score = (claims supported by
context) / (total claims). A low faithfulness score is a hallucination alarm:
the model is asserting things the context doesn't support. For anything
customer-facing or regulated (like banking), this is the metric you watch most.

### Answer Relevancy — catches evasive/padded answers
Generates several hypothetical questions *from the answer*, then measures how
similar they are to the original question. If the answer is on-topic, the
reverse-generated questions resemble the real one. If the answer waffles or
goes off on a tangent, they don't. This is why it needs an embedding model.

### Context Precision vs Context Recall (don't confuse them)
- **Precision**: of what you retrieved, how much was useful, and was the useful
  stuff near the top? Punishes retrieving junk.
- **Recall**: of everything needed to answer, how much did you retrieve? Punishes
  *missing* needed context. Needs a reference answer to know what "everything
  needed" was.

You want both high. High precision + low recall = "clean but incomplete
retrieval." Low precision + high recall = "got everything but buried it in noise."

## Beyond the core four
Newer RAGAS (0.2+) has 35+ metrics, including **Answer Correctness** (vs a
reference answer, combining factual + semantic similarity), **Answer Similarity**,
context entity recall, noise sensitivity, and custom metrics you define yourself
(e.g. a `DiscreteMetric` that returns pass/fail against your own rubric). Start
with the core four; reach for the others when you have a specific question they
answer.

## Where RAGAS fits vs what you already have
| Your existing tool | What it measures |
|---|---|
| Specialist Track Phase 8 (by hand) | Classic IR metrics (P@K, R@K, MRR, NDCG) — retrieval only, needs labels |
| gap-fillers `02_evaluation_harness.ipynb` | Same IR metrics, automated, head-to-head |
| **RAGAS** | LLM-judged quality: faithfulness, answer relevancy, context precision/recall — mostly no labels, grades generation too |

They're complementary, not competing. IR metrics tell you if retrieval found the
right chunks; RAGAS tells you if the *whole system* (including the LLM's answer)
is faithful and relevant. An expert uses both.

## The version situation (read before installing)
RAGAS's API changed across major versions:
- **0.1.x** — older `evaluate()` with a HuggingFace `Dataset`; lots of old tutorials use this
- **0.2.x** — `evaluate()` + `EvaluationDataset` + `SingleTurnSample`; the most
  widely documented stable API, and what this worksheet targets
- **0.3.x / 0.4.x** — newer experiment/dataset abstractions, `llm_factory`,
  `DiscreteMetric`; more powerful but the API is still moving

**Recommendation:** pin `ragas==0.2.x` for stability and to match the worksheet.
`pip install "ragas>=0.2,<0.3" datasets langchain langchain-openai`. Requires
Python 3.10+ (you're on 3.12 — good). If you later adopt a newer version, the
*concepts* here are unchanged; only the function names shift.

## Teaser problem
> Your RAG system scores **Faithfulness 0.95** (excellent — barely hallucinates)
> but **Answer Relevancy 0.55** (poor). The answers are factually grounded but
> users complain they're unhelpful. What's most likely happening, and which part
> of the pipeline do you fix?

**Solution:** high faithfulness + low answer relevancy is the classic signature
of a system that's *retrieving and grounding correctly but answering the wrong
question* — usually because retrieval pulled context that's factually true but
tangential to what the user actually asked, and the LLM dutifully summarized it.
The faithful-but-irrelevant combo points at **retrieval**, not generation: the
answer is faithful to the *retrieved* context, but the retrieved context wasn't
what the question needed. Fix retrieval (better query understanding, re-ranking,
or metadata filtering) before touching the generation prompt. This is exactly the
kind of diagnosis RAGAS enables that a single accuracy number never would — the
worksheet reproduces this scenario.
