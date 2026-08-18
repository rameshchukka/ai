# Evaluation & Guardrails — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

Once an LLM system works once, the real work is making sure it keeps working: automated evals, regression tests, and guardrails that catch bad/unsafe output before it reaches a user.

## What You're About to Learn (and why it matters)

- Building an eval set (input, expected output/criteria) for regression testing
- Using an 'LLM-as-judge' to score subjective outputs
- Guardrails: input validation, output filtering, refusal detection
- Tracking pass/fail rates over prompt or model changes
- Writing a reliability report summarizing eval results

## Before You Start — Quick Mindset Tips

- 💡 Version your eval set like code — it's how you catch regressions when you change a prompt or model.
- 💡 Combine hard checks (exact match, schema validation) with soft checks (LLM judge) where appropriate.
- 💡 Test edge cases deliberately: empty input, adversarial input, out-of-scope questions.
- 💡 A guardrail that blocks too aggressively is also a bug — measure false positive rate too.

## Things That Trip People Up

- 🚧 Only testing the 'happy path' and missing edge cases that show up in production.
- 🚧 Using the same model as both the system-under-test and the judge without sanity-checking judge quality.
- 🚧 Not re-running the eval suite after every prompt/model change.

## Where You'll Actually Use This

- Regression testing a customer support bot before deploying a prompt change
- Content moderation guardrail on generated output
- A triage system's eval suite ensuring consistent classification quality

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
