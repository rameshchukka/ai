# IBM RAG & Agentic AI Certificate — Study Companion (added materials)

This repo is the certificate's lab code, plus study materials I added to help you understand
each lab while taking the course.

## What was added
- **`STUDY_GUIDE.html`** — open in a browser. A companion guide covering every lab:
  the concept behind it, a step-by-step of what the code does, the ideas to understand,
  and how the whole certificate connects (one dataset flows through all modules).
- **Annotated notebooks** — each `.ipynb` now has:
  - a 📘 banner cell at the top explaining it's an annotated reference,
  - 📎 **CONCEPT** callout cells before key code cells, explaining WHAT and WHY.
  The original lab code cells are unchanged — only quoted markdown notes were inserted.

## The labs (one capstone on the California Culinary Map dataset)
| Module | Lab | Concept |
|---|---|---|
| M1L1 | Extract Structured JSON | LLM turns text → typed JSON (structured output) |
| M1L2 | Process Multimodal Data | vision LLM captions images → searchable text |
| M1L3 | CLI Data Management | CRUD hygiene over the dataset |
| M2L1 | Multimodal Vector Index | embed text (384-d) + images (CLIP 512-d) → Chroma |
| M2L2 | Similarity Retrieval + Filtering | semantic search + metadata `where` filter |
| M2L3 | Fusion & Reranking | combine text+image similarity, then rerank |
| M4L1 | Build an MCP Server | expose data (resources) + tools via FastMCP |
| M4L2 | Build an MCP Client | discover + call the server's tools |
| M4L3 | LLM MCP Host | an LLM that uses MCP tools to answer (agentic) |

Stack: **IBM WatsonX (Granite)** LLMs · **CLIP + sentence-transformers** embeddings ·
**Chroma** vector store · **FastMCP** for MCP.

## Important
- These annotated notebooks are for **understanding**. For the **graded submission**, use the
  original lab inside Coursera (the sandbox has the WatsonX credentials + graders wired in).
- **If library installs fail** in the Coursera lab: run the notebook's OWN `%pip install` cell
  (not your own), use `%pip` (percent, not `!pip`), restart the kernel after installing, and if
  it still fails the sandbox may lack internet — re-launch from the graded link or develop in
  Colab and do the final run in the lab.
- The M4 MCP labs are Python files (`server.py`/`client.py`/`app.py`) + `lab-instructions.md`,
  not notebooks — read the instructions and run the server before the client/host.
