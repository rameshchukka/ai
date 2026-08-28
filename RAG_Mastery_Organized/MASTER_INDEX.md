# RAG Mastery — Master Index & Learning Path

You have a large, sprawling set of RAG material accumulated from several sources.
This index organizes all of it into **one ordered learning path**, maps each piece
to the skills in your `Expert_Rag.txt`, and flags what was missing (now added in
`_ADDED_gap_fillers/`).

---

## Part 1 — What you already have, organized by learning stage

### Stage 0 — Foundations (do first if libraries are unfamiliar)
Not in this bundle — lives in your separate `foundations/` zip (numpy, matplotlib,
sklearn). Do that first if array math and plotting aren't second nature yet, since
every visualization here depends on them.

### Stage 1 — Conceptual first contact (pick ONE to start)
| Folder | What it is | Best for |
|---|---|---|
| `07_RAG_Zero_to_Hero/` | Single self-contained notebook, 10 chapters, 100% offline, MockLLM | **Start here** — cleanest linear intro, no API keys, no setup friction |
| `Real_World_Exercises/` | RAG pipeline exercise + a "brain-friendly" plain-language guide + HTML guide | Second pass — same ideas, applied to a realistic scenario |

### Stage 2 — The DeepLearning.AI course (structured fundamentals)
`Retrieval-Augmented-Generation-RAG-main/` — a real graded-style course:
- **Module 1** — RAG Overview + a Python refresher + LLM calls / augmented prompts
- **Module 2** — Information Retrieval foundations: vector embeddings, retrieval
  metrics (precision/recall/cosine/euclidean — with image diagrams), retriever functions
- **Module 3** — Vector databases (uses Weaviate, not Chroma — still valuable, the
  concepts transfer directly)

This is the most *pedagogically rigorous* piece you have — unittests, assignments,
real datasets (`news_data_dedup.csv`). Do it after the zero-to-hero intro.

### Stage 3 — Hands-on with a real vector DB (Chroma-specific)
| Folder | What it is |
|---|---|
| `Chroma_Practice_Lab/` | Your Chroma REST + dataset lab (55-row practice dataset, ingestion, JMeter load tests, conceptual-intuition notebook) |
| `RAG_Visualizer_App/` | Streamlit app to visually explore a Chroma collection |
| `RAG_Pure_Python_and_Wrappers/` | RAG from scratch in pure Python, no framework — the "see every moving part" version |

### Stage 4 — A complete, realistic pipeline
`RAG_Pipeline_Lab_week15/` — the most production-shaped thing you have:
- 6 fictional policy docs (refund, shipping, warranty, escalation, billing, privacy)
- `chunking.py` → `ingest.py` → `retrieve.py` → `generate.py`
- `hybrid_search.py` (BM25 + vector)
- `grounding_stress_test.py` (confirms "I don't know" behavior)
- `integrated_triage.py` (ties it together)
- Real provider switching (Gemini / OpenRouter / mock)

This is your **template for building a real RAG system** — closest to what you'd
ship at work.

### Stage 5 — Systematic skill coverage (reference + drills)
`RAG_Specialist_Track_9Phases/` — the structured track built from your
`Expert_Rag.txt`, one folder per phase, each with concept notes + diagrams +
worksheet. Use this as your **checklist to expert** — see Part 2 for exactly
which phases it covers.

---

## Part 2 — Coverage map against your Expert_Rag.txt

| Expert_Rag phase | Covered by | Status |
|---|---|---|
| **1 — Document Processing** (PDF/DOCX/PPT/HTML/MD/JSON/XML/YAML/CSV/Excel/Swagger) | Specialist Track phase1 | ✅ covered |
| **2 — Chunking** (all 8 strategies) | Specialist Track phase2 + `RAG_Pipeline_Lab_week15/chunking.py` | ✅ covered |
| **3 — Embeddings** (cosine/euclidean/dot, bge/jina/nomic/openai/ST) | Specialist Track phase3 + DeepLearning.AI Module 2 | ✅ covered |
| **5 — Retrieval Techniques** (9 techniques) | Specialist Track phase5 + `hybrid_search.py` | ✅ covered |
| **6 — RAG Patterns** (8 patterns) | Specialist Track phase6 | ⚠️ covered conceptually, but see gap-fillers for runnable CRAG/Adaptive/Multi-hop |
| **7 — Image Retrieval** (OCR, CLIP) | Specialist Track phase7 | ✅ covered |
| **8 — Evaluation** (P@K, R@K, MRR, NDCG, faithfulness) | Specialist Track phase8 + DeepLearning.AI Module 2 (metrics) | ✅ covered |
| **9 — Enterprise Pipelines** (PDF/Swagger/DB/Wiki/Logs → Chroma) | Specialist Track phase9 | ✅ covered |

**Your existing material covers the full Expert_Rag.txt skill list.** The gaps
below are not missing *topics* — they're missing *practice depth* on a few
specific things that separate "understands RAG" from "expert at RAG."

---

## Part 3 — What was missing, now added in `_ADDED_gap_fillers/`

See that folder's own README for details. Summary of what expert RAG needs that
your bundle was light on:

1. **Runnable advanced patterns** — CRAG, Adaptive, Multi-hop, Fusion RAG as
   actual executable notebooks, not just concept notes.
2. **Production concerns** — chunk-size/overlap tuning experiments, retrieval
   failure analysis, embedding drift, cost/latency tradeoffs.
3. **A consolidated evaluation harness** — one notebook that runs P@K, R@K, MRR,
   NDCG, and faithfulness on the same dataset so you can compare retrievers head-to-head.

---

## Recommended order (start to expert)

```
foundations (separate zip: numpy → matplotlib → sklearn)
        │
        ▼
07_RAG_Zero_to_Hero          ← get the whole picture once, offline
        │
        ▼
DeepLearning.AI Modules 1-3  ← rigorous fundamentals, metrics, vector DBs
        │
        ▼
RAG_Pure_Python_and_Wrappers ← see every moving part with no framework
        │
        ▼
Chroma_Practice_Lab          ← hands-on with a real vector DB + your visualizer
        │
        ▼
RAG_Pipeline_Lab_week15      ← build a complete, realistic pipeline
        │
        ▼
RAG_Specialist_Track_9Phases ← systematic phase-by-phase skill coverage
        │
        ▼
_ADDED_gap_fillers           ← the depth that makes you expert, not just competent
```
