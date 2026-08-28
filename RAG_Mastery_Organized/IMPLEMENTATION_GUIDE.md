# RAG Practice — Assessment & Step-by-Step Implementation Guide

You have three practice artifacts covering three flavors of RAG. This guide (1)
assesses each, (2) gives an ordered path through them, and (3) provides detailed
setup — including the Neo4j graph database — so you can actually run them.

The shared source document for all three is `ERP-2008-chapter4.pdf` (a health-care
economics chapter). The sample question they use, *"What is the demand for health?"*,
is answerable from page 2 of that PDF — handy for sanity-checking retrieval.

---

## Part A — Assessment (are these good to practice on?)

### 1. `Building_Conversational_RAG.ipynb` — plain RAG
**Stack:** ChromaDB + SentenceTransformer embeddings + OpenAI/Gemini generation, no
framework (no LangChain/LlamaIndex).
**Verdict: good starting point.** Clean, linear, teaches the fundamentals with nothing
hidden — read file → chunk → embed → store in Chroma → semantic search → feed to LLM.
It's the "see every moving part" version, and it lines up directly with your Chroma
Studio work.
**What's strong:** clear section-by-section flow; uses Chroma (which you already know);
shows the full RAG loop without magic.
**⚠️ Security problem (must fix before running):** this notebook has **two hardcoded API
keys** in it — an OpenAI-style key and a Google key, both live in code cells. See the
security box below; do not run or share it until those are rotated and removed.

### 2. `Building_Conversational_HybridRAG_Pinecone.ipynb` — hybrid RAG
**Stack:** Pinecone (cloud vector DB) + dense (SentenceTransformer) **and** sparse (BM25)
vectors + Gemini, with conversational memory and a RAGAS evaluation section.
**Verdict: the strongest of the three, and the most instructive.** It's well-structured
(numbered steps 1–11), teaches the genuinely important idea of **hybrid search** (dense
meaning + sparse keywords fused with an `alpha` knob), adds conversational memory, and
ends with RAGAS evaluation — tying back to your RAGAS guide.
**What's strong:** keys are read via `os.getenv` (no hardcoding — good hygiene); the
`alpha` dense/sparse trade-off is exactly the hybrid-search concept from your Specialist
Track; the RAGAS section reinforces evaluation.
**Watch-outs:** Pinecone is a **paid cloud service** (has a free tier) and needs an
account + API key; it also reaches out to the internet, so in your org it may be blocked
— you may need to run this one from a personal environment.

### 3. `GraphRAG.zip` — graph-database RAG (Neo4j)
**Stack:** Neo4j (graph DB as vector store) + local HuggingFace `all-mpnet-base-v2`
embeddings + Gemini generation + RAGAS validation + Gradio UI + Docling PDF extraction.
A proper multi-file application, not a notebook.
**Verdict: good, and the most "real project" of the three** — clean separation of
concerns (config / pdf_processor / embeddings / vector_store / response_generator /
validator / orchestrator / app). This is the closest to how you'd structure a production
RAG service.
**Honest caveat about the "graph" part:** despite the name, this app uses Neo4j as a
**vector store**, not as a true knowledge graph. It stores each chunk as an isolated
`:Chunk` node with an embedding and does cosine-similarity search — there are **no
relationships between nodes**, which is what would make it genuine *GraphRAG*. So treat
it as "RAG on top of a graph database" (a great way to learn Neo4j + vector indexes),
not as relationship-aware graph retrieval. That's a fine thing to practice — just know
what it is. The guide's Phase 3 notes how you'd extend it toward real GraphRAG.
**Watch-outs:** needs Neo4j installed/running (covered in detail below); `all-mpnet-base-v2`
is a HuggingFace download, so first run needs a network that isn't blocking HF; Gemini +
Docling both reach the internet.

### Overall
All three are worth practicing, and they form a natural progression: **plain → hybrid →
graph-DB**, increasing in both capability and setup complexity. Do them in that order.

---

## ⚠️ SECURITY — do this first, before anything else

`Building_Conversational_RAG.ipynb` contains **live API keys hardcoded in code cells**
(an OpenAI-style `sk`/`AQ...` key and a Google `AIza...` key). Committing or sharing a
notebook with real keys is a credential leak.

**Do this now:**
1. **Rotate both keys** — revoke the exposed ones and generate new ones (OpenAI dashboard;
   Google AI Studio / Cloud console). Assume the exposed keys are compromised.
2. **Remove them from the notebook** — replace with environment-variable reads:
   ```python
   import os
   openai_key = os.getenv("OPENAI_API_KEY")
   google_key = os.getenv("GOOGLE_API_KEY")
   ```
   and set those in your shell / a `.env` file that is **git-ignored**.
3. **Never commit keys.** Add `.env` to `.gitignore`. The Pinecone and GraphRAG artifacts
   already do this correctly — copy their pattern.

This is the same class of issue as the earlier Insomnia/git leak — the fix is the same:
rotate, remove, and tell whoever owns those accounts if they're organizational.

---

## Part B — Recommended order & prerequisites

```
1. Plain RAG (Chroma)      ← start here; you already know Chroma
        │
        ▼
2. Hybrid RAG (Pinecone)   ← adds sparse+dense fusion, memory, RAGAS
        │
        ▼
3. Graph-DB RAG (Neo4j)    ← full app structure + a new database to set up
```

**Shared prerequisites (all three):**
- Python 3.10–3.12 in a venv (your `chroma_lab_env` works).
- A Google Gemini API key (free tier): https://makersuite.google.com/app/apikey
- The `ERP-2008-chapter4.pdf` in the working folder.

---

## Phase 1 — Plain RAG (Chroma)  ·  `Building_Conversational_RAG.ipynb`

### 1.1 Setup
```bash
lab                     # activate your venv
pip install chromadb PyPDF2 python-docx sentence-transformers google-genai openai
```

### 1.2 Fix the keys (from the security section)
Replace the two hardcoded keys with `os.getenv(...)` reads and set them in your shell:
```bash
export OPENAI_API_KEY="your-rotated-key"     # or skip OpenAI and use only Gemini
export GOOGLE_API_KEY="your-rotated-key"
```

### 1.3 Run, cell by cell
Open in Jupyter/VS Code, run top to bottom. The flow:
1. **Install + imports** — libraries load.
2. **Read file** — `PyPDF2` extracts text from the PDF.
3. **Chunking** — text split into passages.
4. **Setup ChromaDB** — `PersistentClient(path="./chroma_db")`.
5. **Insert** — chunks embedded (SentenceTransformer) + stored.
6. **Semantic search** — query embedded, top-K returned.
7. **RAG query** — top-K chunks fed to the LLM, answer generated.

### 1.4 What to observe
- After insert: the collection count equals your number of chunks.
- Semantic search for *"demand for health"* returns the passage from page 2 of the PDF.
- The final answer cites content from those chunks (not invented).

### 1.5 Connect it to what you know
This is the notebook form of your Chroma Studio datasets — same ingest→embed→store→search
loop. You can even open `./chroma_db` in **Chroma Studio** afterward and browse/visualize
what the notebook stored.

---

## Phase 2 — Hybrid RAG (Pinecone)  ·  `Building_Conversational_HybridRAG_Pinecone.ipynb`

### 2.1 Setup
```bash
pip install pinecone pinecone-text sentence-transformers PyPDF2 google-genai python-dotenv
pip install ragas langchain-google-genai langchain-huggingface datasets   # for the RAGAS section
```

### 2.2 Accounts & keys
- **Pinecone:** sign up at pinecone.io (free "starter" tier), create an API key.
- Put keys in a `.env` (git-ignored):
  ```
  PINECONE_API_KEY=your-pinecone-key
  GOOGLE_API_KEY=your-gemini-key
  ```
- **Org network note:** Pinecone is cloud-hosted — if your org blocks it, run this one
  from a personal machine/network.

### 2.3 The one concept that matters here: `alpha`
Hybrid search fuses two kinds of vectors:
- **Dense** (SentenceTransformer) — captures *meaning*.
- **Sparse** (BM25) — captures *exact keywords*.

`alpha` blends them: `alpha=1` is dense-only, `alpha=0` is sparse-only, `alpha=0.5` is
an even mix. Try the same query at `alpha` 0.0, 0.5, 1.0 and watch the results shift —
keyword-heavy queries (an exact term, a code) do better at low alpha; conceptual queries
do better at high alpha. **This is the whole point of the notebook — spend time here.**

### 2.4 What to observe
- Steps 4–7: dense and sparse vectors built, index created, hybrid vectors upserted.
- Step 8: the `alpha` knob visibly changes which chunks come back.
- Step 10: conversational memory — a follow-up question ("what about its cost?") resolves
  using prior turns.
- Step 11: RAGAS scores (faithfulness, answer relevancy) — ties directly to your RAGAS guide.

### 2.5 Connect it to what you know
The dense+sparse fusion is exactly the hybrid-search concept from Specialist Track Phase 5
and the `hybrid_search.py` in your Week 15 pipeline. The RAGAS section is your `ragas_guide`
applied live.

---

## Phase 3 — Graph-DB RAG (Neo4j)  ·  `GraphRAG/`

This is a full multi-file app. The extra setup is the **Neo4j database** — covered in
detail here.

### 3.1 Install Neo4j (pick ONE option)

**Option A — Neo4j Desktop (easiest for local practice, recommended):**
1. Download Neo4j Desktop: https://neo4j.com/download/
2. Install and open it. Create a **new project**, then **add a Local DBMS**.
3. Set a password (you'll put this in `.env`). Pick a recent 5.x version (needed for the
   vector index).
4. Click **Start** on the DBMS. It listens on `bolt://localhost:7687` by default.
5. (Optional) Open **Neo4j Browser** to run Cypher and watch your data.

**Option B — Docker (clean, reproducible, no desktop app):**
```bash
docker run -d --name neo4j-rag \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your-password-here \
  -e NEO4J_PLUGINS='["apoc"]' \
  neo4j:5.23
```
- `7474` = Neo4j Browser (http://localhost:7474), `7687` = Bolt (what the app connects to).
- Log in at the browser with `neo4j` / `your-password-here`.

**Option C — Neo4j Aura (free cloud tier):** if you can't install locally. Sign up at
neo4j.com/cloud/aura, create a free instance, and use the connection URI/credentials it
gives you. (Cloud, so subject to the same org-network caveat as Pinecone.)

### 3.2 Create the database the app expects
The app's config defaults to a database named `graphragdb`. In Neo4j 5.x Community
Edition you only get the default `neo4j` database, so either:
- **Set `NEO4J_DATABASE=neo4j` in `.env`** (simplest — use the default database), **or**
- If you have Enterprise/Aura that supports multiple DBs, create it in Neo4j Browser:
  ```cypher
  CREATE DATABASE graphragdb
  ```

### 3.3 Fill in `.env`
The zip ships a `.env` template. Set:
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password-here
NEO4J_DATABASE=neo4j          # or graphragdb if you created it
GEMINI_API_KEY=your-gemini-key
HF_TOKEN=your-hf-token         # optional; only needed for gated HF models
```

### 3.4 Python setup
```bash
lab
cd GraphRAG
pip install -r requirements.txt
```
**First-run HuggingFace note:** `all-mpnet-base-v2` downloads from HuggingFace on first
use (~420 MB). If your org blocks HF, download it once on a personal network (it caches to
`~/.cache/huggingface`), or point the app at a locally-saved copy — the same HF-blocking
issue you hit with ChromaFlowStudio.

### 3.5 Understand the vector index
On startup, `vector_store.py` runs `_setup_schema()`, which:
- Creates a uniqueness constraint on `Chunk.id`.
- Creates a **vector index** `chunk_embedding` on `Chunk.embedding` (768 dims, cosine) —
  this needs Neo4j **5.11+**. On older versions it silently falls back to manual cosine
  in Cypher (slower but works). Use 5.x to get the real index.

### 3.6 Run the app
```bash
python app.py
```
Gradio prints a local URL (usually http://127.0.0.1:7860). Open it and:
1. **Upload tab** — upload `ERP-2008-chapter4.pdf`. Watch the console: it chunks, embeds,
   and stores into Neo4j.
2. **Query tab** — ask *"What is the demand for health?"* → it embeds the question,
   searches Neo4j for top-K chunks, and Gemini answers from them.
3. **Validate tab** — runs RAGAS faithfulness + answer relevancy on an answer.
4. **Manage tab** — see document/chunk counts, delete a document.

### 3.7 Watch it in Neo4j Browser (the fun part)
After uploading, run this in Neo4j Browser to *see* what the app stored:
```cypher
MATCH (c:Chunk) RETURN c.source, c.chunk_index, c.text LIMIT 25
```
Count them:
```cypher
MATCH (c:Chunk) RETURN count(c)
```
This is the graph-DB equivalent of Chroma Studio's Browse tab — you're looking at the
raw stored nodes.

### 3.8 What to observe
- Upoad → the chunk count in the Manage tab (and the Cypher count) matches.
- Query → the answer only uses content from the PDF; ask something off-topic and it should
  decline or say it can't find it.
- Validate → faithfulness near 1.0 for a grounded answer; lower if the answer drifts.

### 3.9 From "RAG on a graph DB" toward *real* GraphRAG (stretch goal)
As noted in the assessment, this app stores isolated `:Chunk` nodes with no relationships.
To make it genuine GraphRAG you'd:
1. Extract **entities** from each chunk (e.g. "Medicare", "HSA", "moral hazard") and create
   `(:Entity)` nodes.
2. Link them: `(:Chunk)-[:MENTIONS]->(:Entity)`, and `(:Entity)-[:RELATED_TO]->(:Entity)`.
3. At query time, retrieve by vector **and** traverse relationships to pull in connected
   context (multi-hop) — which is what graph retrieval adds over plain vector search.
This is a substantial extension and a great Phase-4 project once the base app runs.

---

## Part C — Quick reference: what each artifact needs

| | Vector store | Embeddings | LLM | Extra setup | Org-network risk |
|---|---|---|---|---|---|
| Plain RAG | Chroma (local) | SentenceTransformer (local) | OpenAI/Gemini | none | LLM API only |
| Hybrid RAG | Pinecone (cloud) | ST dense + BM25 sparse | Gemini | Pinecone account | Pinecone + Gemini |
| Graph-DB RAG | Neo4j (local/cloud) | all-mpnet (HF, local) | Gemini | Neo4j install + HF download | HF download + Gemini |

**The recurring theme for your org:** local pieces (Chroma, Neo4j, local ST models) are
fine; anything that reaches HuggingFace, Pinecone, or Google may be blocked and need a
personal-network first run or a locally-cached model. Plan around that the same way you
have throughout.

---

## Suggested practice sequence (concrete)

1. **Fix the keys** in the plain-RAG notebook (rotate + `os.getenv`). Non-negotiable first step.
2. **Phase 1** end to end; then open its `./chroma_db` in Chroma Studio to connect it to
   your existing tooling.
3. **Phase 2**, focusing on the `alpha` experiments — run the same query at 0.0 / 0.5 / 1.0.
4. **Phase 3**: install Neo4j (Desktop or Docker), run the app, then explore the stored
   nodes in Neo4j Browser.
5. **Stretch:** attempt the entity-linking extension in 3.9 to turn the Neo4j app into real
   GraphRAG.
