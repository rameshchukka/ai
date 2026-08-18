# Generative AI Fundamentals — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

Generative AI produces new content (text, images, audio) rather than just predicting a label. Modern GenAI is dominated by the Transformer architecture and large-scale pretraining, plus techniques like diffusion for images.

## What You Will Learn

- Tokens & tokenization: how text becomes numbers a model can process
- The Transformer architecture at a high level: self-attention, positional encoding
- Self-attention intuition: how a token 'looks at' other tokens to build context
- Pretraining vs. fine-tuning vs. prompting (three ways to adapt a model)
- Autoregressive text generation: predicting the next token, sampling strategies
- A conceptual overview of diffusion models for image generation
- Key GenAI risks: hallucination, bias, prompt injection, data leakage

## Important Pointers / Tips

- **Tip:** 'Attention' is just a learned weighting of how much each token should influence each other token — that's the core idea underneath the math.
- **Tip:** More tokens in context isn't free — cost and (sometimes) accuracy both suffer with very long contexts.
- **Tip:** Fine-tuning is usually unnecessary for most tasks now — try prompting and RAG first; they're cheaper and faster to iterate on.
- **Tip:** Always assume the model can hallucinate confidently — verification/grounding (RAG, guardrails) is not optional for production use.

## Common Pitfalls

- ⚠️ Treating token count and word count as the same thing (they're not — tokenization varies by model/language).
- ⚠️ Assuming a bigger/newer model automatically fixes a prompting or architecture problem.

## Real-World Use Cases

- Everything in sections 05-11 of this course (LLM APIs, RAG, agents) is applied Generative AI.
- Image generation tools (diffusion models) for design/marketing content.

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
