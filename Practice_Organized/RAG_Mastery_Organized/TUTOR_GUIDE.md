# RAG Mastery — Tutor Guide

A session-by-session path through everything in this bundle. Work top to bottom.
Each session tells you **what to open, what to do, roughly how long, what you should
be able to answer before moving on, and the one trap to avoid.**

Don't rush to move on. The checkpoint questions are the real test — if you can't
answer one in your own words, redo that session before continuing. Reading a
notebook is not the same as understanding it.

---

## How to use this guide

- **One session per sitting.** Most are 45–90 minutes. Don't chain three together;
  spaced practice beats cramming for this material.
- **Run every code cell yourself.** Don't just read outputs. Change a number, break
  something on purpose, see what happens.
- **Keep a scratch file** of questions that come up. Half of expertise is knowing
  what you don't yet understand.
- **Environment:** activate your `chroma_lab_env` (`lab` alias) before launching
  Jupyter/VS Code for anything that touches Chroma or your in-house models. The
  offline notebooks (gap-fillers, playbook, zero-to-hero) run without it.

---

## Stage 0 — Foundations (only if needed)

**Skip if** numpy indexing, matplotlib scatter plots, and sklearn's `fit/transform`
are already comfortable. **Do it if** any of those made you pause in earlier work.

Lives in your separate `foundations/` zip, not this bundle. Order: numpy →
matplotlib → sklearn. Budget ~3 sessions if you do it.

**Checkpoint before leaving Stage 0:** you can, from memory, normalize the rows of
a `(55, 1024)` array, make a 2-panel matplotlib scatter, and explain what
`PCA(n_components=2).fit_transform(X)` returns and its shape.

---

## Stage 1 — See the whole picture once

### Session 1 — Zero to Hero (the 30,000-foot view)
- **Open:** `07_RAG_Zero_to_Hero/RAG_Zero_to_Hero.ipynb`
- **Do:** run all 10 chapters start to finish. It's offline (MockLLM), so nothing
  to configure. Read the theory blocks, don't skip to code.
- **Time:** 90 min.
- **Checkpoint:** explain the full RAG pipeline (ingest → chunk → embed → store →
  retrieve → generate) out loud, and say what the "I don't know" guardrail is for.
- **Trap:** this notebook makes RAG look simple because the data is clean and the
  LLM is mocked. Real RAG is messy — that's what later stages are for. Don't
  mistake "I followed the happy path" for "I understand RAG."

### Session 2 — Real-world framing
- **Open:** `Real_World_Exercises/` — read `User_Guide_BrainFriendly.md` first,
  then `Developer_Guide.md`, then run `EX_RAG_Pipeline_RealWorld.ipynb`.
- **Time:** 60 min.
- **Checkpoint:** name three things that make a real corpus harder than the
  zero-to-hero demo (hint: you'll meet all three again in the Studio Playbook).

---

## Stage 2 — Rigorous fundamentals (the DeepLearning.AI course)

This is the most pedagogically solid material you have. Uses `news_data_dedup.csv`
and has real assignments with `unittests.py`.

### Session 3 — Module 1: RAG Overview
- **Open:** `Retrieval-Augmented-Generation-RAG-main/Module 1 - RAG Overview/`
- **Do:** the Python refresher lab first if you want the warmup, then the
  "Introduction to RAG Systems" assignment, then the LLM-calls/augmented-prompts lab.
- **Time:** 2 sessions (assignment is meaty).
- **Checkpoint:** you can write an augmented prompt by hand that cleanly separates
  "retrieved context" from "the question," and explain why that separation matters.

### Session 4 — Module 2: Retrieval & Search Foundations (the important one)
- **Open:** `.../Module 2 - Information Retrieval and Search Foundations/`
- **Do:** all three parts — Vector Embeddings, Retrieval Metrics, Implementing
  Retriever Functions. The `images/` folders have real diagrams (cosine, euclidean,
  precision/recall) — study them.
- **Time:** 2–3 sessions.
- **Checkpoint:** compute precision@k and recall@k by hand for a small example, and
  explain when cosine vs euclidean vs dot product matters. **This is the single most
  important checkpoint in the whole guide** — retrieval quality is where RAG lives
  or dies.
- **Trap:** it's tempting to skim the metrics. Don't. Every later evaluation you do
  builds on precision/recall/MRR/NDCG from here.

### Session 5 — Module 3: Vector Databases
- **Open:** `.../Module 3 - Information Retrieval with Vector Databases/`
- **Do:** the Weaviate lab. It's a different vector DB than Chroma, but the concepts
  (collections, vector search, metadata filtering) transfer directly.
- **Time:** 60 min.
- **Checkpoint:** explain what a vector database gives you over a plain list of
  vectors + a for-loop (hint: it's not just speed).

---

## Stage 3 — See every moving part with no framework

### Session 6 — Pure Python RAG
- **Open:** `RAG_Pure_Python_and_Wrappers/rag_pure_python.py`
- **Do:** read it top to bottom, then run it. Trace exactly how `chunk_text`,
  `SimpleVectorStore`, and `generate_answer` connect. This is RAG with nothing
  hidden.
- **Time:** 60 min.
- **Checkpoint:** on paper, draw the data flow from a raw string to a final answer,
  naming every function it passes through. If you can do this, no RAG framework will
  ever feel like magic again.

---

## Stage 4 — Hands-on with a real vector DB

### Session 7 — Chroma foundational intuition
- **Open:** `Chroma_Practice_Lab/` — read `BEGINNER_WALKTHROUGH.md`, then run
  `ConceptualIntuition.ipynb`.
- **Do:** follow the walkthrough's numbered steps. This is where you first touch a
  real Chroma database with the practice dataset.
- **Time:** 90 min.
- **Environment:** needs `chroma_lab_env` active + your `inhouse_llm.py` in place.
- **Checkpoint:** you can start a Chroma server, ingest the practice dataset, and
  run a query that returns sensible near-neighbors — and explain why the
  near-duplicate rows land close together.
- **Trap:** the setup friction (venv, paths, server) is real and has nothing to do
  with RAG concepts. Push through it once; it's a one-time cost.

### Session 8 — Explore visually with your own tools
- **Open:** `RAG_Visualizer_App/` (read its README, run `streamlit run app.py`) and
  your separate **Chroma Studio** app.
- **Do:** load the practice dataset, then explore all tabs — Browse, Search,
  Visualize (try 2D and 3D, PCA and UMAP), Cluster drill-down.
- **Time:** 60 min.
- **Checkpoint:** you can look at a 2D projection and say something *true* about the
  data from it (which topics cluster, where duplicates are) — not just "there are
  dots."

---

## Stage 5 — Build a complete, realistic pipeline

### Session 9–10 — The Week 15 pipeline (your work template)
- **Open:** `RAG_Pipeline_Lab_week15/` — read `README.md`, then work the files in
  pipeline order: `chunking.py` → `ingest.py` → `retrieve.py` → `generate.py` →
  `hybrid_search.py` → `grounding_stress_test.py` → `integrated_triage.py`.
- **Do:** run each stage against the 6 policy docs in `docs/`. Actually run the
  grounding stress test and watch it refuse to answer off-topic questions.
- **Time:** 2 sessions.
- **Checkpoint:** you can explain, for this pipeline, exactly where an answer would
  go wrong if (a) chunking were too coarse, (b) retrieval k were too low, (c) the
  grounding instruction were removed. This "where would it break" instinct is
  senior-level.
- **Trap:** this one needs an LLM provider (Gemini/OpenRouter/mock). Start with the
  mock so you're not blocked, then switch to a real provider once the flow is clear.

---

## Stage 6 — Systematic skill coverage (the Specialist Track)

Nine phases, each with concept notes + diagrams + a worksheet. This is your
**checklist to complete coverage** of the Expert_Rag.txt skill set. Do one phase
per session, in this order (numbering matches your source — there's no phase 4).

### Session 11 — Phase 1: Document Processing
- **Open:** `RAG_Specialist_Track_9Phases/phase1_document_processing/` (notes →
  diagrams → worksheet).
- **Checkpoint:** you can extract clean text from a PDF *and* a table, and explain
  why extracting to plain text too early loses information.

### Session 12 — Phase 2: Chunking (the most important phase)
- **Open:** `phase2_chunking/`
- **Checkpoint:** you can name all 8 chunking strategies and, for a given document
  type, pick the right one and defend the choice. Chunking decides retrieval quality
  more than any other single factor.

### Session 13 — Phase 3: Embeddings
- **Open:** `phase3_embeddings/`
- **Checkpoint:** you can explain why one collection must use exactly one embedding
  model, and what breaks if you mix them.

### Session 14 — Phase 5: Retrieval Techniques
- **Open:** `phase5_retrieval_techniques/`
- **Checkpoint:** you can explain hybrid search + RRF and self-query retrieval, and
  say when each earns its added complexity.

### Session 15 — Phase 6: RAG Patterns
- **Open:** `phase6_rag_patterns/`
- **Pair with:** `_ADDED_gap_fillers/01_advanced_patterns_runnable.ipynb` (next
  stage) — the concept notes here, the runnable versions there.
- **Checkpoint:** you can describe when you'd reach for Agentic vs Corrective vs
  Multi-hop RAG rather than plain Naive RAG.

### Session 16 — Phase 7: Image Retrieval
- **Open:** `phase7_image_retrieval/`
- **Checkpoint:** you can explain the difference between OCR+text-embedding and CLIP
  image-embedding, and when to use each.

### Session 17 — Phase 8: Evaluation
- **Open:** `phase8_evaluation/`
- **Pair with:** `_ADDED_gap_fillers/02_evaluation_harness.ipynb`.
- **Checkpoint:** you can explain why high precision + low recall at small k is often
  a "k too small" problem, not a bad-retriever problem.

### Session 18 — Phase 9: Enterprise Pipelines
- **Open:** `phase9_enterprise_pipelines/`
- **Checkpoint:** you can explain the re-sync / upsert problem — what happens to a
  RAG system when a source document is edited or deleted and the pipeline never
  re-runs.

---

## Stage 7 — The depth that makes you expert (gap-fillers)

These run fully offline. Do them after the Specialist Track phases they pair with.

### Session 19 — Advanced patterns, runnable
- **Open:** `_ADDED_gap_fillers/01_advanced_patterns_runnable.ipynb`
- **Do:** run CRAG, Adaptive, Multi-hop, Fusion RAG. Then do the "your turn" —
  swap the mock for your real embedder + LLM.
- **Checkpoint:** you can point to the exact line where each pattern makes its key
  decision (fall back / route / decompose / fuse).

### Session 20 — Evaluation harness
- **Open:** `_ADDED_gap_fillers/02_evaluation_harness.ipynb`
- **Do:** run the head-to-head retriever comparison. Then extend the benchmark to
  more queries.
- **Checkpoint:** you can run this harness on any retriever change and state whether
  the change actually helped, with numbers.

### Session 21 — Production tuning
- **Open:** `_ADDED_gap_fillers/03_production_tuning.ipynb`
- **Do:** the chunk-size and overlap sweeps, and the retrieval failure analysis.
- **Checkpoint:** when an answer is wrong, your first move is to look at the ranked
  retrieval list with scores — not to blame the LLM. Internalize this.

---

## Stage 8 — Capstone: analyze, decide, act

### Session 22 — Chroma Studio Playbook (the integration test)
- **Open:** `_ADDED_Chroma_Studio_Playbook/Chroma_Studio_Playbook.ipynb`
- **Do:** work all 7 sections. For each planted flaw, try to spot it *before*
  reading the diagnosis. Then load `dataset/support_kb.csv` into Chroma Studio and
  find the same problems in the actual app's tabs.
- **Time:** 2 sessions (once with the mock, once with your real embedder for the
  sharper version).
- **Checkpoint (the big one):** given a fresh, unlabelled corpus, you can run the
  full analyze→decide→act loop — coverage, duplicates, cluster-vs-metadata,
  mislabels, overlong docs, collisions, missing metadata — and for each finding,
  name the fix (enrich / dedupe / fix metadata / re-chunk / add filter field).
  **This is the skill real projects and interviews test for.**

---

## After the guide — how to know you're actually expert

You're not done when you've *read* everything. You're done when you can:

1. Take a messy corpus you've never seen and diagnose its retrieval problems using
   the Studio Playbook checklist, without the answer key.
2. Build a RAG pipeline from the Week 15 template and explain every design choice.
3. Change one thing (chunk size, embedding model, retrieval technique) and *prove*
   with the evaluation harness whether it helped.
4. Debug a wrong answer by reading the retrieval list first, and know whether the
   fix is content, chunking, metadata, or retrieval.

If you can do those four on demand, you can crack real RAG work. Come back to the
harder sessions (4, 9–10, 22) periodically — they reward re-doing as your intuition
grows.

---

## Suggested pace

| If you have… | Do… | Finish in… |
|---|---|---|
| 1 hour/day | one session/day | ~4 weeks |
| A weekend intensive | Stages 1–4 Sat, 5–6 Sun | 2 days to a working foundation |
| Only time for the essentials | Sessions 1, 4, 6, 7, 12, 17, 22 | the 20% that gives 80% |

The "essentials" row is the honest minimum to be dangerous: overview, retrieval
metrics, pure-python RAG, real Chroma, chunking, evaluation, and the capstone
playbook. Everything else deepens these.
