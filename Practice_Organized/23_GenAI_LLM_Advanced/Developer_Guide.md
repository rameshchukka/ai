# Generative AI & LLMs — Advanced Topics — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

Beyond calling an API and building basic RAG (sections 05-11): efficient fine-tuning, production-grade vector search, improving retrieval quality with re-ranking, observability for debugging LLM systems in production, defending against prompt injection, and structuring knowledge as a graph.

## What You Will Learn

- Parameter-efficient fine-tuning (LoRA/QLoRA/PEFT) vs. full fine-tuning
- Production vector databases (FAISS, and the tradeoffs vs. Chroma/Pinecone/Weaviate)
- Re-ranking retrieved results with a cross-encoder for higher precision
- LLM observability: tracing prompts/responses/costs/latency across a pipeline
- Prompt injection attacks and mitigation strategies
- Knowledge graphs as a structured complement to vector search
- AI ethics & responsible-AI basics: bias, fairness, transparency

## Important Pointers / Tips

- **Tip:** LoRA trains a small number of additional parameters instead of the whole model — dramatically cheaper than full fine-tuning, and usually sufficient.
- **Tip:** A cross-encoder re-ranker is slower but more accurate than embedding similarity alone — use it on a small top-k shortlist, not the whole corpus.
- **Tip:** Log every LLM call's prompt, response, latency, and token cost from day one — retrofitting observability after an incident is much harder.
- **Tip:** Treat any text an LLM reads (documents, web pages, tool outputs) as untrusted input that could contain injected instructions.
- **Tip:** A knowledge graph shines for structured relationship queries ('who reports to whom') that vector search handles poorly.

## Common Pitfalls

- ⚠️ Fine-tuning when prompting or RAG would have solved the problem more cheaply and with faster iteration.
- ⚠️ Re-ranking the entire corpus instead of just the initial top-k candidates (defeats the performance purpose).
- ⚠️ Treating retrieved/tool-sourced content as trusted instructions rather than untrusted data.

## Real-World Use Cases

- Fine-tuning a small model on a narrow domain task with limited compute (LoRA)
- Large-scale production RAG systems (FAISS/Pinecone + re-ranking)
- Debugging a customer-facing LLM feature via cost/latency/quality tracing
- Enterprise knowledge assistants combining a knowledge graph with vector search

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
