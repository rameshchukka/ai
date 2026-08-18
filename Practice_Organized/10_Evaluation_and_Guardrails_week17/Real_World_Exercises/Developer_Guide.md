# Evaluation & Guardrails — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

Once an LLM system works once, the real work is making sure it keeps working: automated evals, regression tests, and guardrails that catch bad/unsafe output before it reaches a user.

## What You Will Learn

- Building an eval set (input, expected output/criteria) for regression testing
- Using an 'LLM-as-judge' to score subjective outputs
- Guardrails: input validation, output filtering, refusal detection
- Tracking pass/fail rates over prompt or model changes
- Writing a reliability report summarizing eval results

## Important Pointers / Tips

- **Tip:** Version your eval set like code — it's how you catch regressions when you change a prompt or model.
- **Tip:** Combine hard checks (exact match, schema validation) with soft checks (LLM judge) where appropriate.
- **Tip:** Test edge cases deliberately: empty input, adversarial input, out-of-scope questions.
- **Tip:** A guardrail that blocks too aggressively is also a bug — measure false positive rate too.

## Common Pitfalls

- ⚠️ Only testing the 'happy path' and missing edge cases that show up in production.
- ⚠️ Using the same model as both the system-under-test and the judge without sanity-checking judge quality.
- ⚠️ Not re-running the eval suite after every prompt/model change.

## Real-World Use Cases

- Regression testing a customer support bot before deploying a prompt change
- Content moderation guardrail on generated output
- A triage system's eval suite ensuring consistent classification quality

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
