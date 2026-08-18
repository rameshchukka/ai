# Week 14 — LLM Fundamentals & Prompt Engineering (Gemini + OpenRouter Edition)

Lab 1 working files. Supports **Gemini**, **OpenRouter** (pay-as-you-go, works around
Gemini's free-tier rate limits), and a **mock mode** for offline/no-cost practice. Pairs
with:
- `Week14_LLM_Fundamentals_Prompt_Engineering.md` (concept tutorial)
- `Lab1_StepByStep_Guide.md` (concept ↔ exercise walkthrough)
- `GEMINI_NOTES.md` — Gemini-specific API details
- `OPENROUTER_NOTES.md` — OpenRouter setup, model picking, and cost expectations
- `Guided_Labs_UserGuide.html`, Lab 1 section (step-by-step timing + checkpoints)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env: set LLM_PROVIDER, plus the API key for whichever provider you picked
```

## Four modes

| `LLM_PROVIDER` in `.env` | What happens | Cost |
|---|---|---|
| `gemini_auto` (recommended, default) | Tries Gemini free tier first, auto-falls-back to the same Gemini model via OpenRouter if rate-limited/erroring | Free unless it falls back (watch stderr for fallback notices) |
| `gemini` | Real calls to the Gemini API only | Free tier (rate-limited, no fallback) |
| `openrouter` | Real calls via OpenRouter, default model `deepseek/deepseek-chat` | Pay-as-you-go, a few cents for this whole lab |
| `mock` | No API call, no network, no key needed — pre-written responses from `mock_responses.py` | Free, always |

Use `mock` mode to get your code working first, then switch to `gemini_auto` (or `gemini`/
`openrouter` directly) and re-run for the real exercise — the whole point of Exercises 1
and 2 is observing real model behavior, which mock mode can't give you. `gemini_auto`
needs both `GEMINI_API_KEY` and `OPENROUTER_API_KEY` set, since it can use either.

## Files

| File | What it does | Maps to |
|---|---|---|
| `llm_client.py` | Core `call_llm()` wrapper — gemini_auto (Gemini with OpenRouter fallback), gemini, openrouter, or mock | Lab 1, Step 2 |
| `GEMINI_NOTES.md` | Gemini API specifics: system_instruction shape, safety-filter handling, JSON mode, rate limits | Read before Step 2 |
| `OPENROUTER_NOTES.md` | OpenRouter setup, model picking, cost expectations | Read if switching off Gemini |
| `mock_responses.py` | Pre-written mock responses used when `LLM_PROVIDER=mock` | Supports every script |
| `01_temperature.py` | Temperature 0 vs. 1.0 comparison | Lab 1, Step 3 / Exercise 1 |
| `02_classifier.py` | Zero-shot vs. few-shot ticket classification | Lab 1, Step 4 / Exercise 2 |
| `03_cot.py` | Direct answer vs. chain-of-thought on logic problems | Lab 1, Step 5 / Exercise 3 |
| `04_structured_output.py` | JSON extraction + defensive parsing | Lab 1, Step 6 / Exercise 4 |
| `05_context_management.py` | Summarize-then-synthesize stress test | Lab 1, Step 7 / Exercise 5 |
| `06_triage_use_case.py` | Full support-ticket-triage real-world use case | Week 14 tutorial's Real-World Use Case |
| `07_mock_practice.py` | **Mock Response Exercises** — dedicated practice using mock mode: predictable classification tests, defensive parsing against known-good/messy/broken JSON, mock-vs-real comparison | New — see below |

## Run order

```bash
python llm_client.py              # smoke test - confirms your key (or mock mode) works
python 01_temperature.py
python 02_classifier.py
python 03_cot.py
python 04_structured_output.py
python 05_context_management.py
python 06_triage_use_case.py
python 07_mock_practice.py        # always runs in mock mode regardless of .env
```

Each script (except `07_mock_practice.py`) prints its output to the console **and** writes
a `results_*.md` file with a `## Reflection` section for you to fill in — these are the
deliverables Lab 1's checkpoints ask you to commit.

## Before you `git push`

- [ ] `.env` is NOT staged (check with `git status` — it should be ignored)
- [ ] All 6 `results_*.md` files are filled in with **real Gemini output** (not mock output — re-run with `LLM_PROVIDER=gemini` before finalizing)
- [ ] `TEST_MESSAGES` in `02_classifier.py` includes your own 5 new tickets, not just the examples
- [ ] `BILLING_PROBLEMS` in `03_cot.py` includes your own 2 new problems
- [ ] `SAMPLE_TICKETS` in `06_triage_use_case.py` includes your own 5 tickets
- [ ] `07_mock_practice.py`'s Exercise C reflection is filled in
- [ ] This README is committed alongside everything else

## Key learnings (fill in after completing the lab)

- _TODO_
- _TODO_
- _TODO_
