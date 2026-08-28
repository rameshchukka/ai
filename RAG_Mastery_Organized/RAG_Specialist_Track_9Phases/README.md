# RAG-Specialist Track

Built directly from your `Expert_Rag.txt` skill list. Phase numbering matches your
source document exactly (it has no Phase 4, so this track doesn't either). Every
phase is backed by ChromaDB. Where Hugging Face models are genuinely required —
no in-house equivalent exists — they're used directly, per your instruction.

## Structure (same 3-file pattern as the AI Mastery track)
Each phase folder has:
- `concept_notes.md` — theory, comparison tables, a teaser problem + solution
- `diagrams.md` — ASCII diagrams
- `worksheet.ipynb` — hands-on, all storage/retrieval through a real Chroma collection

## Phases

| Phase | Folder | Hugging Face needed? |
|---|---|---|
| 1 — Document Processing | `phase1_document_processing/` | No |
| 2 — Chunking | `phase2_chunking/` | No |
| 3 — Embeddings | `phase3_embeddings/` | **Yes** — BGE, Nomic, Sentence-Transformers downloaded directly |
| 5 — Retrieval Techniques | `phase5_retrieval_techniques/` | No |
| 6 — RAG Patterns | `phase6_rag_patterns/` | No |
| 7 — Image Retrieval | `phase7_image_retrieval/` | **Yes** — CLIP (`openai/clip-vit-base-patch32`) downloaded directly |
| 8 — Evaluation | `phase8_evaluation/` | No |
| 9 — Enterprise Pipelines | `phase9_enterprise_pipelines/` | No |

## Setup
- A running Chroma server (`chroma run --path ./chroma_data --port 8000`) — every
  worksheet connects via `chromadb.HttpClient(host="localhost", port=8000)`, adjust
  to your actual server.
- The **corrected** `inhouse_wrappers.py` (from `wrapper_fix/`) reachable, alongside
  your real `inhouse_llm.py` — each worksheet's setup cell has two `sys.path.append(...)`
  lines to adjust. All worksheets now call `embedder.embed_query()`/`.embed_documents()`
  and `ask()`/`ask_vision()` (defined in the setup cell) instead of `get_embedding(text,
  model=...)` or `multimodal_chat(...)` directly — the originals had a routing bug where
  non-default models silently hit the Qwen3-14B endpoint regardless of `model=`, and the
  vision model had no working client at all. See `wrapper_fix/MIGRATION_NOTES.md` for
  the full explanation.
- Phase-specific installs are called out at the top of each worksheet (`pypdf`,
  `python-docx`, `python-pptx`, `beautifulsoup4`, `lxml`, `PyYAML`, `rank_bm25`,
  `networkx`, and for Phases 3/7: `sentence-transformers`, `transformers`, `torch`,
  `pytesseract` + the Tesseract binary).

## Suggested order
Phases 1 → 2 → 3 build straight on each other (extract → chunk → embed). Phase 5
(retrieval techniques) and Phase 6 (RAG patterns) are best done together since
patterns are built from techniques. Phase 7 (images) and Phase 8 (evaluation) can
be done independently once Phases 1-3 feel solid. Phase 9 (enterprise pipelines)
is the capstone — it reuses chunking strategies from Phase 2 and the ingestion
habits from Phase 5/6, applied to 5 different real source types.

## How every teaser problem is handled
Each `concept_notes.md` ends with a teaser problem + its solution explained.
Each phase's `worksheet.ipynb` reproduces that exact bug/scenario in runnable code
first, then shows the fix — not just described, actually executed against a real
Chroma collection so you see the broken behavior before the corrected behavior.
