# Retrieval-Augmented Generation (RAG) — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

RAG grounds an LLM's answers in your own documents: retrieve relevant chunks, then generate an answer using those chunks as context. It reduces hallucination and lets a model answer questions about private/current data it was never trained on.

## What You Will Learn

- The RAG pipeline: ingest → chunk → embed → store → retrieve → generate
- Document chunking strategies (fixed-size, sentence-aware, overlap)
- Storing/querying a vector store (e.g., Chroma)
- Prompt construction that clearly separates 'retrieved context' from 'question'
- Grounding & citation — telling the model to answer only from context
- Basic RAG evaluation (does the answer match the ground truth / is it grounded?)

## Important Pointers / Tips

- **Tip:** Always instruct the model to say 'I don't know' if the context doesn't contain the answer.
- **Tip:** Use chunk overlap (10-20%) so answers near chunk boundaries aren't cut off.
- **Tip:** Retrieve more chunks than you think you need (k=5-8), then let the model filter relevance.
- **Tip:** Log which chunks were retrieved for every answer — essential for debugging bad answers.
- **Tip:** Re-rank retrieved chunks if you have a re-ranker; raw similarity order isn't always best.

## Common Pitfalls

- ⚠️ Chunking mid-sentence/mid-table and losing meaning.
- ⚠️ Not testing with 'no answer exists' questions — a good RAG system should decline, not invent one.
- ⚠️ Stuffing too much context and burying the actually-relevant chunk.

## Real-World Use Cases

- Internal knowledge-base / policy-document Q&A bot
- Customer support grounded in product documentation
- Legal/contract clause lookup and summarization
- Codebase or technical-docs assistant

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
