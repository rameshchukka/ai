# Evaluation & Guardrails (Week 17)

Lab 4 working files, using the same **Gemini + OpenRouter + mock** setup as Labs 1-3.
Pairs with:
- `Month4_Modern_AI_Agentic_Stack_Course.md` — Week 17 concept notes
- `Guided_Labs_UserGuide.html`, Lab 4 — timing + checkpoints
- `GEMINI_NOTES.md` / `OPENROUTER_NOTES.md` — provider-specific details (same as Labs 1-3)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env: set LLM_PROVIDER=gemini_auto (recommended), plus GEMINI_API_KEY and OPENROUTER_API_KEY
```

## Files

| File | What it does |
|---|---|
| `triage_system.py` | The system under test — self-contained triage prompt (real + deliberately degraded versions), defensive parsing, schema validation |
| `eval_set.json` | 20 test cases, including 5 adversarial/prompt-injection cases |
| `eval_runner.py` | Rule-based eval: schema validity + exact-match urgency checks |
| `llm_judge.py` | LLM-as-judge: rubric-scores the `suggested_first_response` field on 10 cases |
| `regression_test.py` | Runs the eval suite against both the real and degraded prompts, compares pass rates |
| `guardrails.py` | Input guardrail (prompt-injection heuristics) + output guardrail (schema validation), tested against the 5 adversarial cases |
| `mock_responses.py` | **Deterministic, exact-match mock** — keyed by literal ticket text, not keyword heuristics (see below for why) |
| `RELIABILITY_REPORT_TEMPLATE.md` | The actual client-facing deliverable — fill in with your real run's numbers |

## Why this lab's mock mode works differently from Labs 1-3

Labs 1-3's mock files use keyword matching, which is fine for demoing a technique. This
lab's mock is a **direct lookup keyed by exact ticket text**, because eval accuracy testing
needs a known, deterministic answer to validate that `eval_runner.py`'s *own logic* is
correct — before you ever spend a real API call finding out whether your eval code has a
bug versus the model got something wrong. Run the full mock-mode baseline first (should be
20/20), then switch to `gemini_auto` for the real signal.

**Important limitation to know going in:** `regression_test.py` genuinely can't demonstrate
the real regression in pure mock mode, because the mock doesn't vary its answers based on
which system prompt was used. This is explained in the script's docstring and printed as a
note when you run it — the honest result is "no difference detected (expected in mock
mode)," not a fabricated pass/fail. Run it against `gemini_auto` to see the real signal.

## Run order

```bash
python eval_runner.py           # baseline: should show 20/20 in mock mode
python llm_judge.py             # scores 10 cases against a rubric
python regression_test.py       # baseline vs. degraded prompt comparison
python guardrails.py            # tests input/output guardrails on the 5 adversarial cases
```

Then switch `LLM_PROVIDER=gemini_auto` in `.env` and re-run all four — this is where you
find out whether the real triage system's prompt actually resists the adversarial cases,
which mock mode can't tell you.

## Wrap-up

Fill in `RELIABILITY_REPORT_TEMPLATE.md` with your real (non-mock) run's numbers — rename
it to `RELIABILITY_REPORT.md` once complete. This is the deliverable an FDE would actually
hand a client's engineering lead before sign-off.

## Before you `git push`

- [ ] `.env` is NOT staged
- [ ] You've run the full suite against `gemini_auto` at least once, not just mock mode
- [ ] `RELIABILITY_REPORT.md` is filled in with real numbers, not template placeholders
- [ ] `llm_judge.py`'s reflection (do you agree with the judge's scores?) is filled in

## Key learnings (fill in after completing the lab)

- _TODO_
- _TODO_
- _TODO_
