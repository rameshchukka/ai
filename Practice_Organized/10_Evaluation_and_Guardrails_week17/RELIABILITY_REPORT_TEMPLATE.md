# Reliability Report — Support Ticket Triage System

*This is the actual client-facing deliverable an FDE hands over before a system goes to
production. Fill in the sections below using your real run's output — don't just copy the
example numbers, they're placeholders showing the expected shape.*

## System Under Test
- **What it does:** Classifies incoming support tickets by urgency, extracts structured
  metadata, and drafts a suggested first response.
- **Version/prompt:** `TRIAGE_SYSTEM` in `triage_system.py`
- **Eval date:** _TODO_

## Eval Summary
- **Eval set size:** 20 cases (`eval_set.json`), including 5 adversarial/prompt-injection cases
- **Overall pass rate:** _TODO — from `results_baseline.md`_
- **Adversarial-subset pass rate:** _TODO_
- **LLM-as-judge average score:** _TODO — from `results_judge.md`_

## Known Failure Modes
*List anything that failed during your real (non-mock) eval run, and why.*
- _TODO_

## Guardrails In Place
- **Input guardrail:** heuristic prompt-injection detection (`guardrails.py`) — flagged
  _TODO_/5 adversarial cases in testing. Known gap: regex-based detection won't catch every
  injection phrasing; treat as a first layer, not a complete defense.
- **Output guardrail:** schema validation blocks malformed responses from reaching
  downstream systems — reuses the same check as the eval runner.

## Regression Testing
- A degraded-prompt scenario (`TRIAGE_SYSTEM_DEGRADED`, missing the anti-injection
  instruction) was tested via `regression_test.py`.
- **Result:** _TODO — fill in from a real (non-mock) run; mock mode can't demonstrate this
  since it doesn't vary output by system prompt, see regression_test.py's docstring._

## Recommendation
_TODO — is this system ready for production, ready with caveats, or not ready? State your
reasoning in 2-3 sentences, the way you'd actually say it to a client's engineering lead._

---
*Generated as part of Lab 4 — Evaluation & Guardrails. See README.md for how each section's
data was produced.*
