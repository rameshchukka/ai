# RAG Practice Course — Organized

Three RAG exercises (plain → hybrid → graph-database), the guides that explain them,
and six extended examples for deeper practice. All exercises query the same document
(`shared_document/ERP-2008-chapter4.pdf`), so results are directly comparable.

```
00_guides/                 read these first
├── rag_practice_guide.html    concepts + step-by-step + extra practice (open in browser)
└── IMPLEMENTATION_GUIDE.md    the same, in markdown

01_original_exercises/     the three practice builds
├── plain_rag/                 Chroma + SentenceTransformer + LLM (no framework)
├── hybrid_rag/                Pinecone + dense & sparse (BM25) + Gemini + RAGAS
└── graph_rag/                 Neo4j + local embeddings + Gradio app (multi-file)

02_extended_examples/      six runnable scaffolds for deeper practice
├── A_chunking_strategies.ipynb
├── B_alpha_sweep_scored.ipynb
├── C_metadata_filtered_rag.ipynb
├── D_cross_store_comparison.ipynb
├── E_real_graphrag_entities.ipynb
└── F_ragas_tuning_loop.ipynb

shared_document/
└── ERP-2008-chapter4.pdf      the source PDF all exercises use
```

## ⚠️ Before you run anything — security

`01_original_exercises/plain_rag/Building_Conversational_RAG.ipynb` originally shipped
with **two hardcoded API keys**. Before running or sharing it: rotate both keys, and
replace them with `os.getenv(...)` reads backed by a git-ignored `.env`. The full fix is
in the guide's Security section. The other two exercises already use `.env` correctly —
the GraphRAG folder here ships an `.env.template` (no real credentials).

## Start here

1. **Read `00_guides/rag_practice_guide.html`** — concepts first, then the step-by-step.
2. **Do the three original exercises in order:** plain → hybrid → graph-database. Each
   increases in capability and setup complexity.
3. **Then the extended examples** (`02_extended_examples/`) — each targets a concept the
   originals don't fully exercise.

## The three original exercises at a glance

| | Store | Embeddings | LLM | Extra setup | Runs offline? |
|---|---|---|---|---|---|
| plain_rag | Chroma (local) | SentenceTransformer | OpenAI/Gemini | none | needs LLM key |
| hybrid_rag | Pinecone (cloud) | ST dense + BM25 | Gemini | Pinecone account | needs cloud |
| graph_rag | Neo4j (local) | all-mpnet (HF) | Gemini | Neo4j + HF download | needs Neo4j |

Setup for each — including full **Neo4j installation** (Desktop / Docker / Aura) — is in
the guide.

## The six extended examples

Unlike the originals (which need live services), **all six extended scaffolds run offline
out of the box** with a mock embedder — so you can study the *mechanic* immediately, then
swap in real models. Each ends with a "your turn" pointing back to the real exercise and
the relevant part of your wider RAG curriculum.

| Example | Teaches | Builds on |
|---|---|---|
| A · Chunking strategies | fixed vs sentence vs overlap — the highest-impact knob | plain_rag |
| B · Alpha sweep (scored) | measure the dense/sparse blend instead of guessing | hybrid_rag |
| C · Metadata-filtered RAG | scope retrieval by section to kill noise | plain_rag + Chroma Studio |
| D · Cross-store comparison | the vector store is swappable; quality is elsewhere | plain_rag + graph_rag |
| E · Real GraphRAG | add entities + relationships + multi-hop — the real thing | graph_rag (capstone) |
| F · RAGAS tuning loop | measure → change → re-measure, the pro workflow | all + RAGAS |

## Note on the "GraphRAG" exercise

Despite the name, the graph_rag app uses Neo4j as a **vector store** (isolated `:Chunk`
nodes, cosine search) — not a true knowledge graph. It's an excellent way to learn Neo4j
+ vector indexes. **Extended example E** turns it into genuine GraphRAG by adding entity
nodes, relationships, and multi-hop retrieval.

## Org-network reality (recurring theme)

Local pieces (Chroma, Neo4j, local SentenceTransformer models) run fine in your
environment. Anything reaching **HuggingFace** (the graph_rag embedding model),
**Pinecone** (hybrid_rag), or **Google Gemini** (all three) may be blocked — plan a
personal-network first run or a locally-cached model, the same way you have throughout.
