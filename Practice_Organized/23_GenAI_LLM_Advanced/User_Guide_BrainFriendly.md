# Generative AI & LLMs — Advanced Topics — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

Beyond calling an API and building basic RAG (sections 05-11): efficient fine-tuning, production-grade vector search, improving retrieval quality with re-ranking, observability for debugging LLM systems in production, defending against prompt injection, and structuring knowledge as a graph.

## What You're About to Learn (and why it matters)

- Parameter-efficient fine-tuning (LoRA/QLoRA/PEFT) vs. full fine-tuning
- Production vector databases (FAISS, and the tradeoffs vs. Chroma/Pinecone/Weaviate)
- Re-ranking retrieved results with a cross-encoder for higher precision
- LLM observability: tracing prompts/responses/costs/latency across a pipeline
- Prompt injection attacks and mitigation strategies
- Knowledge graphs as a structured complement to vector search
- AI ethics & responsible-AI basics: bias, fairness, transparency

## Before You Start — Quick Mindset Tips

- 💡 LoRA trains a small number of additional parameters instead of the whole model — dramatically cheaper than full fine-tuning, and usually sufficient.
- 💡 A cross-encoder re-ranker is slower but more accurate than embedding similarity alone — use it on a small top-k shortlist, not the whole corpus.
- 💡 Log every LLM call's prompt, response, latency, and token cost from day one — retrofitting observability after an incident is much harder.
- 💡 Treat any text an LLM reads (documents, web pages, tool outputs) as untrusted input that could contain injected instructions.

## Things That Trip People Up

- 🚧 Fine-tuning when prompting or RAG would have solved the problem more cheaply and with faster iteration.
- 🚧 Re-ranking the entire corpus instead of just the initial top-k candidates (defeats the performance purpose).
- 🚧 Treating retrieved/tool-sourced content as trusted instructions rather than untrusted data.

## Where You'll Actually Use This

- Fine-tuning a small model on a narrow domain task with limited compute (LoRA)
- Large-scale production RAG systems (FAISS/Pinecone + re-ranking)
- Debugging a customer-facing LLM feature via cost/latency/quality tracing
- Enterprise knowledge assistants combining a knowledge graph with vector search

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
