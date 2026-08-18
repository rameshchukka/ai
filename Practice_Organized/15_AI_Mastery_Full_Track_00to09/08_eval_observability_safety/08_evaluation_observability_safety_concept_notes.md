# Module 8 — Evaluation, Observability, Safety

## 1. Why evaluation is its own discipline
A demo that "looks right" on 3 hand-picked questions tells you almost nothing
about production behavior. Evaluation means running a representative set of
test cases through your system and scoring them *consistently*, so you can
detect regressions when you change a prompt, model, or chunking strategy.

## 2. RAG/GenAI evaluation metrics (recap + expansion from Module 3)
| Metric | Measures | How to compute without a labeled dataset |
|---|---|---|
| Faithfulness | Answer grounded only in given context | LLM-as-judge: "does this answer use only facts from this context?" |
| Answer relevance | Answer addresses the question | LLM-as-judge or embedding similarity between question and answer |
| Context precision | Retrieved chunks are actually relevant | LLM-as-judge per chunk, or human-labeled relevance if you have it |
| Context recall | All relevant chunks were retrieved | Requires a labeled "gold" relevant-chunk set — harder to automate |
| Latency / cost | Time and token spend per request | Direct instrumentation, no LLM needed |

## 3. LLM-as-judge — strengths and pitfalls
- **Strength**: scales to large eval sets without human labeling.
- **Pitfall — self-preference bias**: a model family can rate its own family's
  outputs more favorably. Use a *different, stronger* model as judge
  (your `MODEL_LLAMA` judging `MODEL_QWEN3_14B` outputs is a reasonable setup).
- **Pitfall — position/verbosity bias**: judges can favor longer or
  first-presented answers regardless of actual quality. Mitigate by
  randomizing presentation order when comparing two candidates.

## 4. Observability — what to log
| Field | Why |
|---|---|
| Request id | Trace one user interaction across retrieval + generation + tool calls |
| Full prompt sent | Can't debug "why did it say that" without seeing the actual prompt |
| Retrieved chunks + scores | Separates retrieval bugs from generation bugs |
| Model + params used | Needed when comparing model versions later |
| Latency per stage | Identifies bottlenecks (retrieval vs generation vs reranking) |
| Final output | The thing you're actually evaluating |

This is the "trace" concept — one request = one trace, broken into spans
(retrieval span, generation span, tool-call span) — the same structure
tools like LangSmith/Arize Phoenix visualize, but you can build a minimal
version yourself with structured logging.

## 5. Safety: guardrails worth testing, not assuming
- **Prompt injection** (Module 1/5): does untrusted retrieved/tool content
  override your system instructions?
- **PII leakage**: does the system ever echo back sensitive data it shouldn't?
- **Refusal correctness**: does it appropriately decline genuinely harmful
  requests without being so trigger-happy it refuses benign ones?
- **Jailbreak resistance**: deliberately try adversarial rephrasings of a
  request you expect it to decline, and confirm it still declines.

## Teaser problem
> Your eval harness shows 95% faithfulness using `MODEL_QWEN3_14B` as its own
> judge. A teammate reruns the same eval set with `MODEL_LLAMA` as judge and
> gets 78%. Which number do you trust, and why?

**Solution:** trust the `MODEL_LLAMA` number more, due to self-preference
bias (section 3) — a model is generally a less skeptical judge of its own
family's outputs. The real fix isn't picking one number, but always using a
judge model from a *different* family/strength tier than the model being
evaluated, and ideally cross-checking with a second judge if the stakes are
high. See the worksheet notebook in this folder for a reproduction of this exact discrepancy.
