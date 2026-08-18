# 📚 RAG (Retrieval-Augmented Generation): Zero to Hero — Guided Lab

Ground an LLM in your own documents: ingest, chunk, embed, index, retrieve, and generate grounded answers with an 'I don't know' guardrail and real evaluation. 100% offline; the architecture matches production RAG exactly.

## The teaching format (every chapter)
- 📖 **Theory** (detailed) — the concept explained properly, not just name-dropped
- 🧠 **Mental model** — the intuition to hold in your head
- 🖼️ **ASCII diagram** — a visual of how it fits together
- 🔬 **Worked example** — runnable code you execute and read
- ⚡ **Pro tips** and ⚠️ **Common traps** — what actually trips people up
- ✏️ **Your Turn** exercise → ✅ **Solution** (revealed right after)

## Chapters
1. Why RAG? (the hallucination problem)
2. The RAG pipeline end-to-end
3. Ingest & chunk documents
4. Embed & index (the vector store)
5. Retrieve relevant chunks
6. Build a grounded prompt
7. Generate the answer
8. Guardrails: I-don't-know & similarity threshold
9. Evaluating a RAG system
10. 🏆 Capstone: complete RAG assistant

## Requirements
```
pip install numpy
```

Prerequisite: the Embeddings & Search lab. Swap embed()->real model, VectorStore->Chroma/FAISS, MockLLM->OpenAI/Gemini for production.

Work top to bottom. Attempt every ✏️ exercise before opening its ✅ solution, and finish with
the 🏆 capstone.
