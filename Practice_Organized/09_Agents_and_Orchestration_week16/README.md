# Agents & Orchestration (Week 16)

Lab 3 working files, using the same **Gemini + OpenRouter + mock** setup as Labs 1-2.
Pairs with:
- `Month4_Modern_AI_Agentic_Stack_Course.md` — Week 16 concept notes
- `Guided_Labs_UserGuide.html`, Lab 3 (Part A + Part B) — timing + checkpoints
- `GEMINI_NOTES.md` / `OPENROUTER_NOTES.md` — provider-specific details (same as Labs 1-2)

## How the agent loop works (read this first)

This lab uses a **portable ReAct-style loop** instead of any single provider's native
function-calling API. On each turn, the model is asked to respond with ONE JSON object —
either a tool call (`{"action": "tool_name", "action_input": {...}}`) or a final answer
(`{"action": "final_answer", "answer": "..."}`) — and the loop executes the requested tool,
feeds the result back as an "Observation," and repeats. This works identically across
Gemini, OpenRouter, and mock mode since it only needs `call_llm(system, user)` — no
provider-specific tool-calling wiring required. (Gemini and OpenAI-compatible APIs also
support native function calling if you want to try that as a stretch goal later — see
`GEMINI_NOTES.md`.)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env: set LLM_PROVIDER=gemini_auto (recommended), plus GEMINI_API_KEY and OPENROUTER_API_KEY
```

## Files — Part A (Tools, Loop, Guardrails)

| File | What it does |
|---|---|
| `mock_data.py` | Fake customer/order database |
| `tools.py` | Tool definitions with Pydantic input schemas: lookup, order status, ticket creation, refund eligibility (placeholder), refund proposal |
| `agent.py` | The core ReAct loop: system prompt builder, defensive JSON action parsing, tool dispatch, max-iteration guard |
| `mock_responses.py` | **Agent-specific** mock responses — scripted multi-step JSON action sequences (different format from Labs 1-2's mock files) |

## Files — Part B (High-Stakes Tools, Human-in-the-Loop, RAG Grounding)

| File | What it does |
|---|---|
| `approval_flow.py` | CLI simulation of human approval — the ONLY place a refund can actually be marked as issued |
| `chunking.py`, `ingest.py`, `retrieve.py`, `generate.py`, `docs/` | Copied from Lab 2 (RAG Pipeline) so this lab is self-contained |
| `integrated_eligibility.py` | Replaces Part A's hardcoded refund-eligibility rules with a real RAG-grounded policy lookup |

## Run order

```bash
# Part A
python agent.py                    # runs 2 built-in test scenarios end to end

# Part B
python ingest.py                   # build the vector index (needed once, reuses Lab 2's docs/)
python integrated_eligibility.py   # compare RAG-grounded eligibility vs. Part A's placeholder
python approval_flow.py            # full agent run + human approval prompt (type y or n when asked)
```

## Try this yourself (Part A, Step 4 — "break it on purpose")

1. In `tools.py`, temporarily rewrite one tool's docstring to be vague or misleading, then
   run `agent.py` again and see how the agent misuses it.
2. Force the max-iteration guard: `python -c "from agent import run_agent; print(run_agent('This is an impossible task that should loop forever.', max_iterations=3))"` —
   confirms the guard fails gracefully instead of hanging.

## A real bug I caught while building this lab

The first version of `mock_responses.py` matched scenarios by scanning the **entire**
scratchpad (task + all prior tool observations), not just the original task. Since
`check_order_status`'s mock observation for `ord_1001` legitimately contains the word
"damaged" (it's real order data), a later iteration of the max-iteration-guard test
accidentally matched the wrong scripted scenario and returned a `final_answer` instead of
looping — which would have silently hidden whether the guard actually worked. Fixed by
matching only against the first `Task:` line. Worth remembering: **your mock data needs
testing too, not just your real integrations** — this is the same lesson Week 17
(Evaluation) applies to production systems.

## Before you `git push`

- [ ] `.env` is NOT staged
- [ ] `chroma_db/` (created by `ingest.py`) is NOT staged — already gitignored
- [ ] You've actually run the "break it on purpose" exercises above, not just read about them
- [ ] The one-paragraph "why refunds aren't fully automated" explanation is written somewhere (add it to this README's bottom, or a separate notes file)

## Key learnings (fill in after completing the lab)

- _TODO_
- _TODO_
- _TODO_
