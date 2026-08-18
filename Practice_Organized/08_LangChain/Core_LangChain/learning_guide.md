# Capstone Learning Roadmap — RAG / GenAI / MCP / Agentic AI

Uses your in-house models exclusively, fully offline-safe (no Hugging Face downloads).

## Project files (in order of study)

| File | Teaches | Frameworks used |
|---|---|---|
| `llm_provider.py` | Bridging your org's models (or real OpenAI on your personal laptop) into LangChain's interfaces | LangChain base classes + your inhouse endpoints, no Hugging Face |
| `rag_pure_python.py` | What RAG *actually does* under the hood | none |
| `rag_langchain_faiss.py` | RAG with LangChain abstractions, simplest vector store | LangChain + FAISS |
| `rag_langchain_chroma.py` | RAG with a persistent, production-style vector DB | LangChain + Chroma |

Study them in that order. Each one removes a layer of "what is the framework doing for me" — by the time you reach Chroma, you'll know exactly what `.from_documents()` and `.as_retriever()` are doing internally, because you wrote it by hand in step 1.

## Phase-by-phase plan

### Phase 1 — Foundations (Week 1)
- Run `rag_pure_python.py` line by line. Print intermediate values (chunk list, embedding vector shape, similarity scores).
- Swap `chunk_size`/`overlap` and observe how retrieval quality changes.
- **Model used:** `MODEL_JINA` (embeddings), `MODEL_QWEN3_14B` (generation).

### Phase 2 — Framework fluency (Week 1–2)
- Run `rag_langchain_faiss.py`, then `rag_langchain_chroma.py`.
- Replace the demo string with a real PDF (use `PyPDFLoader`) and a real question set.
- Compare FAISS vs Chroma: persistence, metadata filtering, delete-by-id.
- **Exercise:** add `MODEL_QWEN3_30B` as a second LLM and compare answer quality on the same retrieved chunks — your first taste of model evaluation.

### Phase 3 — Multimodal RAG (Week 2)
- Extend the pipeline: when a chunk's source page contains an image/chart, route it through `multimodal_chat` with `model=MODEL_QWEN2_5_VL_7B` to get a text description, then embed *that* description with Jina alongside regular text chunks.
- This is the "multimodal" piece of your capstone — image content becomes retrievable text.

### Phase 4 — MCP (Week 3)
- Wrap one tool (e.g., your retriever, or a calculator/SQL query function) as an MCP server using the `mcp` Python SDK.
- Write a small client that: takes a user question → asks `MODEL_QWEN3_14B` to decide whether to call the MCP tool → dispatches to the MCP server → feeds the tool result back to the model for the final answer.
- Use `MODEL_DEVSTRAL` while you're writing/debugging the MCP server code itself — it's your in-house coding-specialist model.

### Phase 5 — Agentic AI (Week 3–4)
- Build a ReAct-style loop: model proposes an action (retrieve / call MCP tool / answer), you execute it, feed the observation back, repeat until it answers.
- Use `MODEL_QWEN3_30B` as the agent brain for anything requiring multi-step planning; fall back to `MODEL_QWEN3_14B` for simpler single-hop questions — a good exercise in routing by task complexity.

### Phase 6 — Evaluation (ongoing)
- Use `MODEL_LLAMA` (70B) as a "judge" model: feed it the question, retrieved context, and answer from a smaller model, and ask it to score faithfulness/relevance 1–5. This is a standard RAG-eval pattern and a good capstone deliverable (a small eval harness, not just a demo).

## Model cheat-sheet (quick reference)

| Model | Use for |
|---|---|
| `MODEL_JINA` | All embeddings (RAG retrieval) |
| `MODEL_QWEN3_14B` | Default chat/generation, simple agent steps |
| `MODEL_QWEN3_30B` | Harder reasoning, multi-step agent planning |
| `MODEL_MISTRAL` | Cross-checking prompt behavior vs Qwen family |
| `MODEL_LLAMA` (70B) | Judge/evaluator for scoring other models' RAG answers |
| `MODEL_DEVSTRAL` | Writing/debugging MCP servers, tool code, agent scaffolding |
| `MODEL_QWEN2_5_VL_7B` | Image/chart understanding for multimodal RAG |

## Capstone deliverable shape (suggestion)
By the end, you'd have: a document ingestion pipeline (Phase 1–3) → an MCP-exposed tool layer (Phase 4) → an agent that decides when to retrieve vs call a tool vs answer directly (Phase 5) → an eval script that scores it (Phase 6). That maps cleanly onto "RAG + GenAI + MCP + Agentic AI" as one coherent system rather than four separate demos.
