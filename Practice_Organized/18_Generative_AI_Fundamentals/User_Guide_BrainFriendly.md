# Generative AI Fundamentals — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

Generative AI produces new content (text, images, audio) rather than just predicting a label. Modern GenAI is dominated by the Transformer architecture and large-scale pretraining, plus techniques like diffusion for images.

## What You're About to Learn (and why it matters)

- Tokens & tokenization: how text becomes numbers a model can process
- The Transformer architecture at a high level: self-attention, positional encoding
- Self-attention intuition: how a token 'looks at' other tokens to build context
- Pretraining vs. fine-tuning vs. prompting (three ways to adapt a model)
- Autoregressive text generation: predicting the next token, sampling strategies
- A conceptual overview of diffusion models for image generation
- Key GenAI risks: hallucination, bias, prompt injection, data leakage

## Before You Start — Quick Mindset Tips

- 💡 'Attention' is just a learned weighting of how much each token should influence each other token — that's the core idea underneath the math.
- 💡 More tokens in context isn't free — cost and (sometimes) accuracy both suffer with very long contexts.
- 💡 Fine-tuning is usually unnecessary for most tasks now — try prompting and RAG first; they're cheaper and faster to iterate on.
- 💡 Always assume the model can hallucinate confidently — verification/grounding (RAG, guardrails) is not optional for production use.

## Things That Trip People Up

- 🚧 Treating token count and word count as the same thing (they're not — tokenization varies by model/language).
- 🚧 Assuming a bigger/newer model automatically fixes a prompting or architecture problem.

## Where You'll Actually Use This

- Everything in sections 05-11 of this course (LLM APIs, RAG, agents) is applied Generative AI.
- Image generation tools (diffusion models) for design/marketing content.

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
