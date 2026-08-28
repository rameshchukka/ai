# Retrieval-Augmented Generation (RAG) — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

RAG grounds an LLM's answers in your own documents: retrieve relevant chunks, then generate an answer using those chunks as context. It reduces hallucination and lets a model answer questions about private/current data it was never trained on.

## What You're About to Learn (and why it matters)

- The RAG pipeline: ingest → chunk → embed → store → retrieve → generate
- Document chunking strategies (fixed-size, sentence-aware, overlap)
- Storing/querying a vector store (e.g., Chroma)
- Prompt construction that clearly separates 'retrieved context' from 'question'
- Grounding & citation — telling the model to answer only from context
- Basic RAG evaluation (does the answer match the ground truth / is it grounded?)

## Before You Start — Quick Mindset Tips

- 💡 Always instruct the model to say 'I don't know' if the context doesn't contain the answer.
- 💡 Use chunk overlap (10-20%) so answers near chunk boundaries aren't cut off.
- 💡 Retrieve more chunks than you think you need (k=5-8), then let the model filter relevance.
- 💡 Log which chunks were retrieved for every answer — essential for debugging bad answers.

## Things That Trip People Up

- 🚧 Chunking mid-sentence/mid-table and losing meaning.
- 🚧 Not testing with 'no answer exists' questions — a good RAG system should decline, not invent one.
- 🚧 Stuffing too much context and burying the actually-relevant chunk.

## Where You'll Actually Use This

- Internal knowledge-base / policy-document Q&A bot
- Customer support grounded in product documentation
- Legal/contract clause lookup and summarization
- Codebase or technical-docs assistant

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
