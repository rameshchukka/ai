# Module 1 — Generative AI Core

## 1. Prompting techniques
| Technique | What it does | When to use |
|---|---|---|
| Zero-shot | Instruction only, no examples | Simple, well-known tasks |
| Few-shot | 2-5 examples before the real input | Need consistent format/style; model isn't reliable zero-shot |
| Chain-of-Thought (CoT) | Ask model to reason step by step before answering | Multi-step math/logic, anything with intermediate reasoning |
| Self-consistency | Sample CoT multiple times, take majority answer | High-stakes single answer, willing to pay extra calls for accuracy |
| ReAct | Interleave reasoning with tool actions | Agentic tasks (Module 5) |

## 2. Sampling parameters
- **temperature**: scales the logit distribution before sampling. Near 0 →
  near-deterministic, picks the highest-probability token almost always.
  Higher (0.7-1.0+) → more diverse/creative, more risk of incoherence.
- **top-p (nucleus sampling)**: only sample from the smallest set of tokens
  whose cumulative probability ≥ p. Adapts to how "confident" the model is.
- **top-k**: only sample from the k most likely tokens, regardless of probability mass.
- **max_tokens**: hard cap on output length — doesn't affect quality, just truncates.

**Note on your in-house stack:** check whether `multimodal_chat` exposes
`temperature`/`top_p` as parameters. If it only exposes `max_tokens`, the
server-side default sampling is fixed — worth confirming with whoever built
`inhouse_llm.py` if you need more deterministic or more creative output.

## 3. Structured output / function calling
Two ways to get structured data out of a model:
1. **Prompt-level**: instruct "respond with ONLY valid JSON matching this
   schema," then parse and validate. Fragile but works with any model.
2. **Native function/tool calling**: model is given a tool schema and trained
   to emit a structured call object rather than free text. More reliable, but
   only works if the model/serving stack explicitly supports it (check if
   your vLLM/serving setup exposes an OpenAI-compatible `tools` parameter).

## 4. Multimodal (vision-language) basics
A vision-language model (your `MODEL_QWEN2_5_VL_7B`) encodes an image into a
sequence of vision tokens, projects them into the same embedding space as
text tokens, and processes both with the same transformer. Practically: you
pass image bytes/base64 alongside text, and the model attends across both.

## 5. Model family decision tree
See the diagrams file in this folder for the full decision tree. Quick version using your stack:
- Need raw chat/reasoning → `MODEL_QWEN3_14B` (default) or `MODEL_QWEN3_30B` (harder reasoning)
- Need code generation/debugging → `MODEL_DEVSTRAL`
- Need to understand an image/chart → `MODEL_QWEN2_5_VL_7B`
- Need a vector for retrieval → `MODEL_JINA`
- Need a second opinion / evaluator → `MODEL_LLAMA` (70B, generally strongest)

## Teaser problem
> You ask the model for JSON three times and get three slightly different
> formats — sometimes with markdown fences, sometimes with extra prose before
> the JSON. Why, and how do you fix it without an output-parsing library?

**Solution:** the model isn't being constrained, only asked nicely. Fix:
(1) put the schema and "ONLY valid JSON, no fences, no extra text" in the
**system** prompt, not buried in the user prompt — system instructions get
more weight; (2) give one concrete example of the exact output format
(few-shot, see section 1); (3) as a safety net, strip code fences with a
one-line `.strip("`").replace("json\\n","")` before `json.loads`. See
the worksheet notebook in this folder section 3 for this fixed live.
