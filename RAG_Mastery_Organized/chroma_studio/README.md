# Chroma Studio

A local ChromaFlowStudio-style tool built specifically for **chromadb 1.5.9** and
your environment — full create / update / delete of documents and collections,
plus graph & cluster visualization. Unlike ChromaFlowStudio, it does **not** force
a HuggingFace download, and it lets you switch embedding source in the UI.

Every CRUD and visualization path in this app was executed against a real
chromadb 1.5.9 database before shipping — not just syntax-checked.

## What it does
- **Browse** — page through a collection's documents + metadata, filter by text
- **Add** — one at a time or bulk (one document per line)
- **Edit / Update** — change a document's text (re-embeds) or just its metadata (no re-embed)
- **Delete** — individual documents, or whole collections
- **Visualize** — PCA, t-SNE, or UMAP projection in **2D or 3D** (3D is rotatable), color by metadata field or by KMeans cluster, with cluster drill-down. 2D is usually enough; use 3D to spot-check clusters that look merged in 2D.
- **Manage** — create collections (choice of cosine / l2 / ip distance), delete collections

## Setup
```bash
# from inside your chroma_lab_env venv (the one with chromadb 1.5.9)
pip install -r requirements.txt
```
If you plan to use the local sentence-transformers embedding option, also:
```bash
pip install sentence-transformers
```

## Run
```bash
streamlit run app.py
```
Then in the sidebar:
1. **Local Chroma folder** — point at the folder containing `chroma.sqlite3`
   (e.g. `D:\ChromaFlowStudio\ChromaDB_data`). Only one app can hold a local
   Chroma folder at a time — close ChromaFlowStudio / other notebooks first.
2. **Embedding source** — pick one:
   - **In-house Jina (hosted)** — enter your Jina base URL + API key. No download,
     no HuggingFace. This is the default to use in your environment.
   - **Local model (sentence-transformers)** — enter a model name or a local
     folder path. A *folder path* avoids any HuggingFace download; a bare model
     name will try to download from HuggingFace on first use (which your org
     blocks), so download it once on an unblocked network first, or point at the
     folder where you saved a downloaded Jina model.

## Important notes
- **Embeddings are only called when you add/update documents.** Browsing and
  deleting never touch the embedder — so even if the embedding source is
  misconfigured or blocked, you can still manage existing data.
- **One embedding source per collection.** Don't add vectors from two different
  models into the same collection — mixing vector spaces breaks similarity search.
  Create a separate collection per model.
- **Local folder = one process at a time.** This uses `PersistentClient`, which
  holds an exclusive lock on `chroma.sqlite3`. If you get a lock/connection
  error, another app is already using that folder.
- The Jina base URL / dimension defaults match your `inhouse_llm.py`
  (`jina-embeddings-v3`, dimension 1024, OpenAI-style `/embeddings` endpoint).
  Change them in the sidebar if your values differ.

## Files
- `app.py` — the Streamlit app
- `embedding_backends.py` — the two switchable embedding sources
- `requirements.txt` — pinned to chromadb 1.5.9
