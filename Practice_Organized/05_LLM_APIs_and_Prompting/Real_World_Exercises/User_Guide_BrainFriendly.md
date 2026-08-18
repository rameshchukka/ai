# LLM APIs & Prompt Engineering — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

Calling an LLM API well is a skill: structuring prompts, controlling output format, managing context length/cost, and handling failures gracefully. This is the interface layer between your code and models like GPT/Gemini.

## What You're About to Learn (and why it matters)

- Making basic completion/chat calls and reading the response structure
- System vs. user vs. assistant roles, and why system prompts matter
- Temperature, top_p, and other sampling parameters and their effect on output
- Prompt patterns: zero-shot, few-shot, chain-of-thought
- Getting reliable structured output (JSON mode / schema-constrained generation)
- Context window management — summarizing/truncating long conversations
- Basic error handling & retries for rate limits and timeouts

## Before You Start — Quick Mindset Tips

- 💡 Be explicit about output format in the prompt ('respond with ONLY valid JSON, no prose').
- 💡 Lower temperature (0–0.3) for factual/deterministic tasks; higher (0.7+) for creative tasks.
- 💡 Few-shot examples in the prompt often beat lengthy instructions for format consistency.
- 💡 Always validate/parse model output defensively — never trust it's perfectly formed.

## Things That Trip People Up

- 🚧 Vague prompts producing inconsistent output shape across calls.
- 🚧 Not handling API errors/rate limits — a demo that works once and breaks under load.
- 🚧 Assuming the model 'remembers' previous calls — you must resend conversation history.
- 🚧 Blindly trusting hallucinated facts/citations without a grounding step (see RAG).

## Where You'll Actually Use This

- Automated support ticket triage/classification
- Structured data extraction from unstructured text (invoices, resumes, emails)
- Summarization pipelines for long documents
- A chain-of-thought reasoning assistant for multi-step business logic

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
