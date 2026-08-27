# Chroma Navigator

A single-file Streamlit tool to **browse**, **search**, and **visually
explore** a local Chroma vector database — built specifically to plug into
your in-house embedding model rather than relying on Chroma's default
(Hugging Face-downloading) embedding function.

## Why this instead of an existing tool
Existing community tools (chromadb-admin, ChromaFlowStudio, chroma-ui, etc.)
are good at CRUD-style browsing but don't show you the embedding space
itself. Generic embedding visualizers (TensorFlow Projector, Atlas) show the
space but don't know about Chroma or your custom embedder. This combines
both, with a 4th tab for KMeans cluster drill-down — directly continuing the
visualization work from notebook 01 in the capstone project, but interactive
and reusable for any collection.

## Setup

```bash
pip install -r requirements.txt --break-system-packages
```

Place `app.py` in the same folder as your existing `inhouse_wrappers.py` and
`inhouse_llm.py` (from the `inhouse_rag_capstone` project), or edit the
`sys.path.append(...)` line near the top of `app.py` to point at that folder.

## Run

```bash
streamlit run app.py
```

In the sidebar, choose **Connect via**:

- **HTTP server** — use this if you started Chroma as a standalone server,
  e.g. `chroma run --path ./chroma_db --port 8080`. Enter the **Host**
  (`localhost` if it's running on your machine, or the server's address/IP
  if remote) and **Port** (whatever you passed to `chroma run`, or your
  container/k8s service port). Check **Use HTTPS** if the server sits behind
  TLS. If the server has token auth enabled, expand **Auth (optional)** and
  paste the bearer token — adjust the header name in `app.py` if your server
  uses a different auth scheme.
- **Local persist directory** — use this if you're using `PersistentClient`
  directly from a script (no server process), e.g. the `./chroma_db` folder
  created by `rag_langchain_chroma.py` or notebook `07`.

Either way, once connected you'll see the same collection dropdown and all
four tabs below.

## Tabs

- **Browse** — table of every id/document/metadata field in the selected
  collection, with a text filter.
- **Search** — type a query, it's embedded with your in-house Jina model via
  `InHouseEmbeddings`, and top-k nearest documents are shown with distances.
- **Visualize** — 2D or 3D PCA (or UMAP, if installed) projection of every
  embedding in the collection, as an interactive Plotly scatter. Hover for
  a text preview, color by any metadata field, zoom/rotate.
- **Cluster drill-down** — runs KMeans over the raw embeddings, colors the
  same projection by cluster, and lets you select one cluster to read every
  document in it — useful for spotting duplicate or mis-chunked content.

## Notes
- Works on any existing Chroma collection regardless of which embedding
  model created it — only the **Search** tab needs `InHouseEmbeddings` (to
  embed new queries consistently with what's stored). Browse/Visualize/Cluster
  work on the vectors already stored in Chroma.
- For very large collections (100k+ items), replace the `collection.get(...)`
  call in `load_collection()` with paginated `limit`/`offset` calls — loading
  everything into memory at once won't scale past a certain size.
