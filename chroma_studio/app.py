"""
Chroma Studio — a local CRUD + visualization tool for Chroma 1.5.9
===================================================================
A ChromaFlowStudio-style app, but built for chromadb==1.5.9 and your
environment (no forced HuggingFace download; switchable embedding source).

Run with:  streamlit run app.py

Connects to a LOCAL Chroma database folder via PersistentClient (one app at a
time holds the lock). Full create/add, edit/update, delete, plus graph &
cluster visualization.
"""

import json
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import chromadb

from embedding_backends import build_embedder

st.set_page_config(page_title="Chroma Studio", layout="wide", page_icon="◧")

# ---------------------------------------------------------------------------
# Minimal, non-templated styling — cool slate + a single amber action accent.
# ---------------------------------------------------------------------------
st.markdown("""
<style>
  :root { --ink:#1b2430; --slate:#5b6b7d; --line:#dde3ea; --amber:#c77d49; }
  .stApp { background:#f7f9fb; }
  h1, h2, h3 { color:#1b2430; letter-spacing:-0.01em; }
  .studio-tag { color:#7a8a9a; font-size:0.82rem; text-transform:uppercase;
                letter-spacing:0.14em; margin-bottom:-0.3rem; }
  .rowcount { font-variant-numeric:tabular-nums; font-weight:600; color:#1b2430; }
  div[data-testid="stMetricValue"] { font-variant-numeric:tabular-nums; }
  .stButton button { border-radius:6px; }
</style>
""", unsafe_allow_html=True)


# ===========================================================================
# Connection + embedding source (sidebar)
# ===========================================================================
st.sidebar.markdown("### Database")
persist_dir = st.sidebar.text_input(
    "Local Chroma folder",
    value=r"D:\ChromaFlowStudio\ChromaDB_data",
    help="The folder containing chroma.sqlite3. One app can hold this at a time.",
)

st.sidebar.markdown("### Embedding source")
emb_source_label = st.sidebar.radio(
    "Where embeddings come from",
    ["In-house Jina (hosted)", "Local model (sentence-transformers)"],
    help="Adding/updating documents needs an embedder. Browsing/deleting does not.",
)

emb_kwargs = {}
if emb_source_label.startswith("In-house"):
    emb_source = "jina_hosted"
    # Defaults match your inhouse_llm.py; edit if your values differ.
    emb_kwargs["base_url"] = st.sidebar.text_input(
        "Jina base URL",
        value="https://llm-api.iservebetter.idfcfirstbank.com/jina-embeddings-v3/v1",
    )
    emb_kwargs["api_key"] = st.sidebar.text_input("API key", value="", type="password")
    emb_kwargs["dimension"] = st.sidebar.number_input("Dimension", value=1024, step=1)
else:
    emb_source = "local_st"
    emb_kwargs["model_name_or_path"] = st.sidebar.text_input(
        "Model name or local path",
        value="all-MiniLM-L6-v2",
        help="A local folder path avoids any HuggingFace download. To use a "
             "downloaded Jina model, point this at its folder.",
    )

st.sidebar.caption(
    "Embeddings only get called when you add or update documents, or run a text "
    "search. Browsing and deleting never call the embedder — so a missing/blocked "
    "model won't stop you managing existing data."
)


@st.cache_resource(show_spinner=False)
def get_client(path: str):
    return chromadb.PersistentClient(path=path)


def get_embedder_safe():
    """Build the embedder only when actually needed, surfacing a clear error
    instead of crashing the whole app if it can't be constructed."""
    try:
        return build_embedder(emb_source, **emb_kwargs), None
    except Exception as e:
        return None, str(e)


try:
    client = get_client(persist_dir)
    connection_ok = True
    connection_err = None
except Exception as e:
    connection_ok = False
    connection_err = str(e)


# ===========================================================================
# Header
# ===========================================================================
st.markdown('<div class="studio-tag">Chroma 1.5.9 · local</div>', unsafe_allow_html=True)
st.title("Chroma Studio")

if not connection_ok:
    st.error(
        f"Can't open the Chroma folder at `{persist_dir}`.\n\n"
        f"**What happened:** {connection_err}\n\n"
        "**Likely fixes:** confirm the path points at the folder containing "
        "`chroma.sqlite3`, and make sure no other app (ChromaFlowStudio, another "
        "notebook) is holding that folder open — only one process can use a local "
        "Chroma folder at a time."
    )
    st.stop()


def list_collection_names():
    # Chroma 1.5.9: list_collections() returns collection objects.
    return [c.name for c in client.list_collections()]


collection_names = list_collection_names()


# ===========================================================================
# Collection selector + collection-level actions
# ===========================================================================
left, right = st.columns([3, 1])
with left:
    if collection_names:
        selected = st.selectbox("Collection", collection_names)
    else:
        selected = None
        st.info("No collections yet. Create one in the **Manage** tab below to get started.")
with right:
    st.metric("Collections", len(collection_names))


def open_collection(name: str):
    """Open WITHOUT an embedding_function for browse/delete (never triggers the
    embedder). For add/update/search we re-open WITH the embedder."""
    return client.get_collection(name=name)


# ===========================================================================
# Tabs
# ===========================================================================
tab_browse, tab_add, tab_edit, tab_viz, tab_manage = st.tabs(
    ["Browse", "Add", "Edit / Update", "Visualize", "Manage"]
)


# ---------------------------------------------------------------------------
# BROWSE
# ---------------------------------------------------------------------------
with tab_browse:
    if not selected:
        st.stop()
    coll = open_collection(selected)
    total = coll.count()
    st.markdown(f'<span class="rowcount">{total}</span> documents in '
                f'<code>{selected}</code>', unsafe_allow_html=True)

    limit = st.slider("How many to load", 5, min(500, max(5, total)) if total else 5,
                      min(50, total) if total else 5)
    data = coll.get(limit=limit, include=["documents", "metadatas"])

    if data["ids"]:
        rows = []
        for i, _id in enumerate(data["ids"]):
            row = {"id": _id, "document": data["documents"][i] if data["documents"] else ""}
            meta = data["metadatas"][i] if data["metadatas"] else None
            if meta:
                for k, v in meta.items():
                    row[f"meta.{k}"] = v
            rows.append(row)
        df = pd.DataFrame(rows)

        q = st.text_input("Filter rows (plain text match across all columns)", "")
        if q:
            mask = df.apply(lambda r: r.astype(str).str.contains(q, case=False).any(), axis=1)
            df = df[mask]
            st.caption(f"{len(df)} of {total} rows match '{q}'")
        st.dataframe(df, use_container_width=True, height=440)
    else:
        st.info("This collection is empty. Add documents in the **Add** tab.")


# ---------------------------------------------------------------------------
# ADD
# ---------------------------------------------------------------------------
with tab_add:
    if not selected:
        st.stop()
    st.subheader("Add documents")
    st.caption("Adds new documents to the selected collection. Their embeddings are "
               "computed by the embedding source you picked in the sidebar.")

    mode = st.radio("Input mode", ["One at a time", "Bulk (one document per line)"],
                    horizontal=True)

    if mode == "One at a time":
        new_id = st.text_input("ID", value="", placeholder="e.g. doc_001")
        new_text = st.text_area("Document text", height=120)
        meta_str = st.text_input("Metadata as JSON (optional)", value="",
                                 placeholder='{"topic": "cooking"}')
        if st.button("Add document", type="primary"):
            if not new_id or not new_text.strip():
                st.warning("Give the document both an ID and some text.")
            else:
                embedder, err = get_embedder_safe()
                if embedder is None:
                    st.error(f"Couldn't build the embedder, so the document wasn't added.\n\n{err}")
                else:
                    try:
                        metadata = json.loads(meta_str) if meta_str.strip() else None
                        vec = embedder([new_text])[0]
                        coll = open_collection(selected)
                        coll.add(ids=[new_id], embeddings=[vec], documents=[new_text],
                                 metadatas=[metadata] if metadata else None)
                        st.success(f"Added '{new_id}'. Collection now has {coll.count()} documents.")
                    except json.JSONDecodeError:
                        st.error("Metadata isn't valid JSON. Example: {\"topic\": \"cooking\"}")
                    except Exception as e:
                        st.error(f"Add failed: {e}")

    else:
        bulk = st.text_area("One document per line", height=200)
        id_prefix = st.text_input("ID prefix", value="doc")
        if st.button("Add all lines", type="primary"):
            lines = [l.strip() for l in bulk.splitlines() if l.strip()]
            if not lines:
                st.warning("Nothing to add — the box is empty.")
            else:
                embedder, err = get_embedder_safe()
                if embedder is None:
                    st.error(f"Couldn't build the embedder, so nothing was added.\n\n{err}")
                else:
                    try:
                        coll = open_collection(selected)
                        start = coll.count()
                        ids = [f"{id_prefix}_{start + i}" for i in range(len(lines))]
                        vecs = embedder(lines)
                        coll.add(ids=ids, embeddings=vecs, documents=lines)
                        st.success(f"Added {len(lines)} documents. Collection now has {coll.count()}.")
                    except Exception as e:
                        st.error(f"Bulk add failed: {e}")


# ---------------------------------------------------------------------------
# EDIT / UPDATE
# ---------------------------------------------------------------------------
with tab_edit:
    if not selected:
        st.stop()
    st.subheader("Edit or update a document")
    st.caption("Change a document's text or metadata. Updating the text re-computes "
               "its embedding via the sidebar's embedding source.")

    coll = open_collection(selected)
    existing = coll.get(include=["documents", "metadatas"])
    if not existing["ids"]:
        st.info("Nothing to edit — this collection is empty.")
    else:
        target_id = st.selectbox("Document ID", existing["ids"])
        idx = existing["ids"].index(target_id)
        current_text = existing["documents"][idx] if existing["documents"] else ""
        current_meta = existing["metadatas"][idx] if existing["metadatas"] else {}

        edited_text = st.text_area("Text", value=current_text, height=120)
        edited_meta = st.text_input("Metadata as JSON",
                                    value=json.dumps(current_meta) if current_meta else "")

        col_u, col_d = st.columns(2)
        with col_u:
            if st.button("Save changes", type="primary"):
                try:
                    metadata = json.loads(edited_meta) if edited_meta.strip() else None
                    text_changed = edited_text != current_text
                    if text_changed:
                        embedder, err = get_embedder_safe()
                        if embedder is None:
                            st.error(f"Text changed but the embedder couldn't be built, "
                                     f"so nothing was saved.\n\n{err}")
                            st.stop()
                        vec = embedder([edited_text])[0]
                        coll.update(ids=[target_id], embeddings=[vec],
                                    documents=[edited_text],
                                    metadatas=[metadata] if metadata else None)
                    else:
                        # Metadata-only change: no embedding recompute needed.
                        coll.update(ids=[target_id],
                                    metadatas=[metadata] if metadata else None)
                    st.success(f"Saved changes to '{target_id}'.")
                except json.JSONDecodeError:
                    st.error("Metadata isn't valid JSON.")
                except Exception as e:
                    st.error(f"Update failed: {e}")
        with col_d:
            if st.button("Delete this document"):
                try:
                    coll.delete(ids=[target_id])
                    st.success(f"Deleted '{target_id}'. Reopen the tab to refresh the list.")
                except Exception as e:
                    st.error(f"Delete failed: {e}")


# ---------------------------------------------------------------------------
# VISUALIZE
# ---------------------------------------------------------------------------
with tab_viz:
    if not selected:
        st.stop()
    st.subheader("Visualize the embedding space")
    coll = open_collection(selected)
    total = coll.count()
    if total < 3:
        st.info("Add at least 3 documents to visualize — projection needs a few points.")
    else:
        got = coll.get(limit=total, include=["documents", "metadatas", "embeddings"])
        vectors = np.array(got["embeddings"])
        ids = got["ids"]
        docs = got["documents"] or ["" for _ in ids]
        metas = got["metadatas"] or [{} for _ in ids]

        c1, c2, c3 = st.columns(3)
        with c1:
            method = st.radio("Projection", ["PCA (fast)", "t-SNE", "UMAP"],
                              help="PCA: fast, linear. t-SNE/UMAP: slower, tighter clusters.")
        with c2:
            dims = st.radio("Dimensions", [2, 3],
                            help="3D is rotatable (click-drag). 2D is easier to read and "
                                 "usually enough — use 3D to spot-check clusters that look "
                                 "merged in 2D.")
        with c3:
            meta_keys = sorted({k for m in metas if m for k in m.keys()})
            color_by = st.selectbox("Color points by", ["(none)", "KMeans cluster"] + meta_keys)

        # --- project to 2 or 3 dimensions ---
        from sklearn.decomposition import PCA
        if method.startswith("PCA"):
            coords = PCA(n_components=dims).fit_transform(vectors)
        elif method.startswith("t-SNE"):
            from sklearn.manifold import TSNE
            perp = max(2, min(30, len(ids) // 3))
            coords = TSNE(n_components=dims, perplexity=perp, random_state=42).fit_transform(vectors)
        else:  # UMAP
            try:
                import umap
                coords = umap.UMAP(n_components=dims, random_state=42).fit_transform(vectors)
            except ImportError:
                st.error("UMAP isn't installed. Run `pip install umap-learn`, or pick PCA / t-SNE.")
                st.stop()

        # --- determine colors ---
        if color_by == "KMeans cluster":
            from sklearn.cluster import KMeans
            k = st.slider("Number of clusters (k)", 2, min(12, len(ids) - 1), min(5, len(ids) - 1))
            labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(vectors)
            color_vals = [f"cluster {l}" for l in labels]
        elif color_by != "(none)":
            color_vals = [str(m.get(color_by, "—")) if m else "—" for m in metas]
        else:
            color_vals = ["all" for _ in ids]

        hover = [f"{i}<br>{(d[:80] + '…') if len(d) > 80 else d}" for i, d in zip(ids, docs)]
        legend_title = color_by if color_by != "(none)" else ""
        if dims == 2:
            fig = px.scatter(
                x=coords[:, 0], y=coords[:, 1], color=color_vals,
                hover_name=ids, hover_data={"text": hover},
                labels={"x": "dim 1", "y": "dim 2", "color": legend_title},
            )
            fig.update_traces(marker=dict(size=11, line=dict(width=0.5, color="white")))
        else:
            fig = px.scatter_3d(
                x=coords[:, 0], y=coords[:, 1], z=coords[:, 2], color=color_vals,
                hover_name=ids, hover_data={"text": hover},
                labels={"x": "dim 1", "y": "dim 2", "z": "dim 3", "color": legend_title},
            )
            fig.update_traces(marker=dict(size=5, line=dict(width=0.5, color="white")))
        fig.update_layout(height=620 if dims == 3 else 560, legend_title_text="",
                          plot_bgcolor="#ffffff", paper_bgcolor="#ffffff")
        st.plotly_chart(fig, use_container_width=True)
        if dims == 3:
            st.caption("Click-drag to rotate, scroll to zoom. Hover a point to read the chunk.")

        # --- cluster drill-down ---
        if color_by == "KMeans cluster":
            st.markdown("#### What's inside each cluster")
            pick = st.selectbox("Inspect cluster", sorted(set(color_vals)))
            for i, c in enumerate(color_vals):
                if c == pick:
                    st.write(f"**{ids[i]}** — {docs[i][:140]}")


# ---------------------------------------------------------------------------
# MANAGE (create / delete collections)
# ---------------------------------------------------------------------------
with tab_manage:
    st.subheader("Manage collections")

    st.markdown("**Create a collection**")
    st.caption("A collection is created with the current sidebar embedding source. "
               "Keep one embedding source per collection — mixing models in one "
               "collection breaks similarity search.")
    new_coll_name = st.text_input("New collection name", value="",
                                  placeholder="e.g. my_documents")
    space = st.selectbox("Distance metric", ["cosine", "l2", "ip"], index=0,
                         help="cosine is the usual choice for text embeddings.")
    if st.button("Create collection", type="primary"):
        if not new_coll_name.strip():
            st.warning("Give the collection a name.")
        else:
            try:
                client.get_or_create_collection(
                    name=new_coll_name.strip(),
                    metadata={"hnsw:space": space},
                )
                st.success(f"Created '{new_coll_name}'. Select it above to start adding documents.")
            except Exception as e:
                st.error(f"Couldn't create the collection: {e}")

    st.divider()
    st.markdown("**Delete a collection**")
    st.caption("Deletes the whole collection and every document in it. This can't be undone.")
    if collection_names:
        to_delete = st.selectbox("Collection to delete", collection_names, key="del_coll")
        confirm = st.checkbox(f"Yes, permanently delete '{to_delete}' and all its documents")
        if st.button("Delete collection"):
            if not confirm:
                st.warning("Tick the confirmation box first.")
            else:
                try:
                    client.delete_collection(name=to_delete)
                    st.success(f"Deleted '{to_delete}'. Refresh the page to update the list.")
                except Exception as e:
                    st.error(f"Delete failed: {e}")
    else:
        st.info("No collections to delete yet.")
