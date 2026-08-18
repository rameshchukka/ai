# LLM APIs & Prompt Engineering — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

Calling an LLM API well is a skill: structuring prompts, controlling output format, managing context length/cost, and handling failures gracefully. This is the interface layer between your code and models like GPT/Gemini.

## What You Will Learn

- Making basic completion/chat calls and reading the response structure
- System vs. user vs. assistant roles, and why system prompts matter
- Temperature, top_p, and other sampling parameters and their effect on output
- Prompt patterns: zero-shot, few-shot, chain-of-thought
- Getting reliable structured output (JSON mode / schema-constrained generation)
- Context window management — summarizing/truncating long conversations
- Basic error handling & retries for rate limits and timeouts

## Important Pointers / Tips

- **Tip:** Be explicit about output format in the prompt ('respond with ONLY valid JSON, no prose').
- **Tip:** Lower temperature (0–0.3) for factual/deterministic tasks; higher (0.7+) for creative tasks.
- **Tip:** Few-shot examples in the prompt often beat lengthy instructions for format consistency.
- **Tip:** Always validate/parse model output defensively — never trust it's perfectly formed.
- **Tip:** Log prompts + responses during development; you can't debug what you can't see.
- **Tip:** Keep a mental 'token budget' — long context costs money and can degrade attention to instructions.

## Common Pitfalls

- ⚠️ Vague prompts producing inconsistent output shape across calls.
- ⚠️ Not handling API errors/rate limits — a demo that works once and breaks under load.
- ⚠️ Assuming the model 'remembers' previous calls — you must resend conversation history.
- ⚠️ Blindly trusting hallucinated facts/citations without a grounding step (see RAG).

## Real-World Use Cases

- Automated support ticket triage/classification
- Structured data extraction from unstructured text (invoices, resumes, emails)
- Summarization pipelines for long documents
- A chain-of-thought reasoning assistant for multi-step business logic

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
