# RAG Pipeline (Week 15 — Retrieval-Augmented Generation)

Lab 2 working files, using the same **Gemini + OpenRouter + mock** setup as the LLM
Fundamentals lab. Pairs with:
- `Month4_Modern_AI_Agentic_Stack_Course.md` — Week 15 concept notes
- `Guided_Labs_UserGuide.html`, Lab 2 (Part A + Part B) — timing + checkpoints
- `Lab2_StepByStep_Guide.md` — concept ↔ exercise walkthrough
- `GEMINI_NOTES.md` / `OPENROUTER_NOTES.md` — provider-specific details (same as Lab 1)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env: set LLM_PROVIDER=gemini_auto (recommended), plus GEMINI_API_KEY and OPENROUTER_API_KEY
```

No API key is needed for embeddings — `ingest.py` uses a local
`sentence-transformers` model, so embedding is free and works offline regardless of
`LLM_PROVIDER`. API calls only happen in `generate.py`, `grounding_stress_test.py`, and
`integrated_triage.py` (the actual answer-generation steps) — those are where
`LLM_PROVIDER` actually matters.


## Files — Part A (Ingestion, Embeddings, Retrieval)

| File | What it does |
|---|---|
| `docs/*.txt` | 6 fictional policy documents (refund, shipping, warranty, escalation, billing, data privacy) |
| `chunking.py` | Splits documents into overlapping chunks with source metadata |
| `ingest.py` | Embeds chunks and stores them in a local ChromaDB collection |
| `retrieve.py` | Queries the vector store, compares top-k=1 vs top-k=5 |
| `hybrid_search.py` | Stretch goal: BM25 keyword search combined with vector search |

## Files — Part B (Generation, Grounding & Citations)

| File | What it does |
|---|---|
| `generate.py` | Full RAG pipeline: retrieve → augment → generate, with citations |
| `grounding_stress_test.py` | Confirms the system refuses to answer questions not covered in the docs |
| `integrated_triage.py` | Wires RAG into a Week-14-style triage system; before/after comparison |

## Run order

```bash
# Part A
python chunking.py              # sanity-check chunks
python ingest.py                # build the vector index (run this first, always)
python retrieve.py              # test retrieval quality
python hybrid_search.py         # optional stretch goal

# Part B (requires ingest.py to have been run)
python generate.py              # grounded answers with citations
python grounding_stress_test.py # refusal/hallucination check
python integrated_triage.py     # before/after comparison vs. Week 14
```

## Before you `git push`

- [ ] `.env` and `chroma_db/` are NOT staged (both are gitignored — confirm with `git status`)
- [ ] `docs/` folder is committed (and ideally also uploaded to your storage bucket per the Guided Labs setup)
- [ ] `results_grounding.md` and `before_after_comparison.md` reflections are filled in
- [ ] `PART_A_NOTES.md` written (chunk size rationale, retrieval observations)
- [ ] `KNOWN_ANSWER_QUERIES` / `UNANSWERABLE_QUESTIONS` reviewed — add your own if you want extra practice

## Key learnings (fill in after completing the lab)

- _TODO_
- _TODO_
- _TODO_
