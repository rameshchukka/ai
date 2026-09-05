# LangChain Practice — Organized

Your seven LangChain archives, organized into one structure with an easy-to-follow HTML
guide in every folder. Three are your own practice folders (01–03); four are external
courses/repos, each with an orienting guide.


## Guides in this bundle

- **`DEVELOPMENT_GUIDE.html`** (root) — set up your Mac/Windows desktop: Python, venv, dependencies, keys, editor, org-network provider choices. **Read this first.**
- **A detailed `GUIDE_*.html` in every folder** — concepts, step-by-step walkthrough, and worked answers / expected output for each exercise. Open the one for the folder you're in.

```
01_Models/                    YOUR practice — LLM & embedding models
├── GUIDE_01_Models.html
02_Prompts/                   YOUR practice — prompt & chat templates
├── GUIDE_02_Prompts.html
03_Core_and_Extensions/       YOUR capstone — RAG/GenAI/Agentic, in-house models
├── GUIDE_03_Core_and_Extensions.html
├── Core_LangChain/           RAG: pure Python → FAISS → Chroma  (+ GUIDE)
├── Extensions/               7 notebooks: GenAI & Agentic, with/without LangChain (+ GUIDE)
└── Real_World_Exercises/     applied exercises (ships its own guide)
04_external_courses/          third-party courses (each keeps its own README)
├── deeplearning_ai_short_course/   DeepLearning.AI L1–L6 notebooks
├── learning_langchain_book/        "Learning LangChain" book code, ch1–ch10
├── langchain_cookbook/             Cookbook + topic tutorials (large reference)
└── langchain_chatbot_app/          a deployable chatbot app (reference architecture)
```

## ⚠️ Security — read first

`01_Models/.env` and `02_Prompts/.env` originally contained **live API keys** (a Google
key in both, plus a HuggingFace token in 01_Models). In this organized copy those values
have been **emptied**. Before running anything:
1. **Rotate** the original keys — revoke the exposed ones and generate new. Assume the
   exposed keys are compromised.
2. Put fresh keys in your local `.env` files.
3. Never commit real keys — keep `.env` git-ignored.

## Suggested learning path

Easiest → most involved. The first three are YOUR own material and come first:

1. **`01_Models`** — how LangChain wraps any LLM/embedding provider behind one interface.
2. **`02_Prompts`** — prompt templates and chat message roles (system/human/AI) + history.
3. **`03_Core_and_Extensions`** — your capstone. Core (RAG pure-Python → FAISS → Chroma),
   then the 7 Extensions notebooks (GenAI & Agentic, each *without* then *with* LangChain),
   then Real-World Exercises. Wired to your in-house models — the safest to run on the org
   network. Start with its `GUIDE_03_Core_and_Extensions.html`.
4. **`04_external_courses/deeplearning_ai_short_course`** — DeepLearning.AI L1–L6 notebooks.
5. **`04_external_courses/learning_langchain_book`** — the most comprehensive; ch1→ch10.
6. **`04_external_courses/langchain_cookbook`** — reference to dip into.
7. **`04_external_courses/langchain_chatbot_app`** — last: a real deployable app.

Open each folder's `GUIDE_*.html` in a browser when you reach it.

## How this connects to your RAG work

LangChain is the framework version of things you've already built by hand:
- `01_Models/document_similarity.py` is the kernel of RAG (embed → cosine → rank) — the same
  idea your Chroma/pgvector exercises scale up with a vector database.
- The DeepLearning.AI **L4 (Q&A)** and **L5 (Evaluation)** notebooks map onto your RAG and
  RAGAS material.
- Seeing RAG both ways — from scratch (your pure-Python work) and via a framework (here) —
  is exactly what makes the framework stop feeling like magic.

## Org-network note

Scripts default to cloud providers (OpenAI/Google/Anthropic) and some pull from HuggingFace.
On your org network these may be blocked — use the local HuggingFace options
(`chatmodel_hf_local.py`, `embedding_hf_local.py`) where possible, or adapt the model line to
your in-house wrapper. The LangChain interface stays the same regardless of provider.
