# AI Mastery — Zero to Hero

10 modules, each with the same 3-file structure, with the concept baked into
every filename (so files are unambiguous even outside their folder):
- `<concept>_concept_notes.md` — theory, comparison tables, teaser problem + solution
- `<concept>_diagrams.md` — ASCII diagrams (flows, type hierarchies, architecture)
- `<concept>_worksheet.ipynb` — hands-on practice, including the teaser problem reproduced live

Work through them in order — each builds on the last.

| # | Folder | Files prefixed with | Core question it answers |
|---|---|---|---|
| 00 | `00_foundations/` | `00_tokens_embeddings_transformers_attention_` | What actually happens between "text in" and "text out"? |
| 01 | `01_genai_core/` | `01_genai_core_prompting_sampling_structured_output_` | How do you reliably control what a model produces? |
| 02 | `02_embeddings_vector_search/` | `02_embeddings_vector_search_` | How does similarity search actually work, and where does it break? |
| 03 | `03_rag/` | `03_rag_ingestion_retrieval_generation_` | How do you ground generation in retrieved truth, and debug it when it isn't? |
| 04 | `04_langchain_internals/` | `04_langchain_lcel_memory_runnables_` | What is the framework actually doing for you vs. doing yourself? |
| 05 | `05_agentic_ai/` | `05_agentic_ai_react_reflexion_multiagent_` | How does an LLM decide what to do next, and when does that go wrong? |
| 06 | `06_mcp/` | `06_mcp_model_context_protocol_` | How do you make a tool reusable across any agent/app, not just yours? |
| 07 | `07_vector_relational_db/` | `07_vector_db_plus_relational_db_` | When do you need both, and how do you join them correctly? |
| 08 | `08_eval_observability_safety/` | `08_evaluation_observability_safety_` | How do you know your system is actually working, at scale? |
| 09 | `09_productionizing/` | `09_productionizing_caching_streaming_scaling_` | What turns a working demo into something that survives real users? |

## Setup
Most worksheets import from `inhouse_wrappers.py`, `inhouse_llm.py`, and
`rag_pure_python.py` from your earlier `inhouse_rag_capstone` project. Either:
- copy those 3 files into this folder, or
- adjust the `sys.path.append(...)` line in each worksheet's setup cell to
  point at wherever they live.

Module 6 additionally needs `pip install mcp --break-system-packages`.
Module 7 additionally needs `pip install chromadb psycopg2-binary --break-system-packages`.

## How to use the teaser problems
Each `concept_notes.md` ends with a "Teaser problem" — read it, try to answer
it yourself first, *then* read the solution underneath. Each corresponding
worksheet reproduces the bug/scenario live in code so you see the failure
mode, not just the explanation of it.
