"""
Chroma Navigator
=================
A single-file Streamlit app to browse, search, and visually explore a
local Chroma vector database — using your in-house embedding model for
any new query embedding (via InHouseEmbeddings from inhouse_wrappers.py).

Run:
    streamlit run app.py

Place this file in the same folder as inhouse_wrappers.py / inhouse_llm.py
(or edit the import path below), and point it at your existing
persist_directory (e.g. the ./chroma_db folder created by
rag_langchain_chroma.py or notebook 07).
"""

import os
import sys
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import chromadb

# --- adjust this if app.py lives elsewhere relative to your wrappers ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from inhouse_wrappers import InHouseEmbeddings
    from inhouse_llm import MODEL_JINA
    EMBEDDER = InHouseEmbeddings(model=MODEL_JINA)
    EMBEDDER_AVAILABLE = True
except Exception as e:
    EMBEDDER_AVAILABLE = False
    EMBEDDER_ERROR = str(e)

st.set_page_config(page_title="Chroma Navigator", layout="wide")
st.title("🔭 Chroma Navigator")
st.caption("Browse collections, run searches, and visually explore the embedding space.")

# ---------------------------------------------------------------------------
# Sidebar: connection
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Connection")
    conn_mode = st.radio("Connect via", ["HTTP server", "Local persist directory"], horizontal=False)

    if conn_mode == "HTTP server":
        host = st.text_input("Host", value="localhost")
        port = st.number_input("Port", value=8080, min_value=1, max_value=65535, step=1)
        ssl = st.checkbox("Use HTTPS (ssl)", value=False)
        # Optional, only needed if your Chroma server has auth enabled
        with st.expander("Auth (optional)"):
            auth_token = st.text_input("Bearer/auth token", value="", type="password")
    else:
        persist_dir = st.text_input("Chroma persist directory", value="./chroma_db")

    connect_clicked = st.button("Connect", type="primary")

    if not EMBEDDER_AVAILABLE:
        st.warning(
            "Could not import InHouseEmbeddings — query search will be disabled "
            "(browsing/visualization of existing vectors still works).\n\n"
            f"Error: {EMBEDDER_ERROR if not EMBEDDER_AVAILABLE else ''}"
        )

if "client" not in st.session_state or connect_clicked:
    try:
        if conn_mode == "HTTP server":
            kwargs = {"host": host, "port": int(port), "ssl": ssl}
            if auth_token:
                # Adjust header name to match your server's auth provider
                # (Chroma's token auth provider expects "Authorization: Bearer <token>")
                kwargs["headers"] = {"Authorization": f"Bearer {auth_token}"}
            client = chromadb.HttpClient(**kwargs)
            client.heartbeat()  # raises if unreachable — fail fast with a clear error
            st.session_state.client = client
        else:
            if os.path.isdir(persist_dir):
                st.session_state.client = chromadb.PersistentClient(path=persist_dir)
            else:
                st.sidebar.error(f"Path not found: {persist_dir}")
                st.stop()
    except Exception as e:
        st.sidebar.error(f"Could not connect: {e}")
        st.stop()

client = st.session_state.get("client")
if client is None:
    st.info("Enter connection details in the sidebar and click Connect.")
    st.stop()

collections = client.list_collections()
if not collections:
    st.warning("No collections found in this directory.")
    st.stop()

collection_names = [c.name for c in collections]
selected_name = st.sidebar.selectbox("Collection", collection_names)
collection = client.get_collection(selected_name)

count = collection.count()
st.sidebar.metric("Items in collection", count)

# ---------------------------------------------------------------------------
# Pull all data once (fine for capstone-scale collections; for huge ones,
# add pagination via collection.get(limit=..., offset=...))
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading collection...")
def load_collection(_collection, name, n):
    data = _collection.get(include=["documents", "metadatas", "embeddings"])
    return data

data = load_collection(collection, selected_name, count)
ids = data["ids"]
documents = data["documents"] or [""] * len(ids)
metadatas = data["metadatas"] or [{}] * len(ids)
embeddings = np.array(data["embeddings"]) if data.get("embeddings") is not None else None

df = pd.DataFrame({
    "id": ids,
    "document": documents,
})
meta_df = pd.json_normalize(metadatas) if metadatas and any(metadatas) else pd.DataFrame(index=range(len(ids)))
df = pd.concat([df, meta_df], axis=1)

tab_browse, tab_search, tab_visualize, tab_cluster = st.tabs(
    ["📄 Browse", "🔎 Search", "🗺️ Visualize", "🧩 Cluster drill-down"]
)

# ---------------------------------------------------------------------------
# TAB 1: Browse
# ---------------------------------------------------------------------------
with tab_browse:
    st.subheader(f"Collection: {selected_name}")
    text_filter = st.text_input("Filter by text in document (substring)", "")
    shown = df[df["document"].str.contains(text_filter, case=False, na=False)] if text_filter else df
    st.dataframe(shown, use_container_width=True, height=500)
    st.caption(f"Showing {len(shown)} of {len(df)} items")

# ---------------------------------------------------------------------------
# TAB 2: Search
# ---------------------------------------------------------------------------
with tab_search:
    st.subheader("Semantic search")
    query = st.text_input("Query", "")
    k = st.slider("Top-k", 1, 20, 5)
    if query and EMBEDDER_AVAILABLE:
        q_vec = EMBEDDER.embed_query(query)
        results = collection.query(query_embeddings=[q_vec], n_results=k,
                                    include=["documents", "metadatas", "distances"])
        res_df = pd.DataFrame({
            "id": results["ids"][0],
            "distance": results["distances"][0],
            "document": results["documents"][0],
        })
        st.dataframe(res_df, use_container_width=True)
    elif query and not EMBEDDER_AVAILABLE:
        st.error("Embedder not available — fix the import at the top of app.py to enable search.")

# ---------------------------------------------------------------------------
# TAB 3: Visualize embedding space
# ---------------------------------------------------------------------------
with tab_visualize:
    st.subheader("Embedding space (dimensionality-reduced)")
    if embeddings is None or len(embeddings) == 0:
        st.warning("This collection has no stored embeddings to visualize.")
    else:
        method = st.radio("Reduction method", ["PCA", "UMAP (if installed)"], horizontal=True)
        dims = st.radio("Dimensions", [2, 3], horizontal=True)
        color_field = st.selectbox(
            "Color by", ["(none)"] + [c for c in meta_df.columns] if not meta_df.empty else ["(none)"]
        )

        if method == "PCA":
            from sklearn.decomposition import PCA
            reducer = PCA(n_components=dims)
            coords = reducer.fit_transform(embeddings)
        else:
            try:
                import umap
                reducer = umap.UMAP(n_components=dims, random_state=42)
                coords = reducer.fit_transform(embeddings)
            except ImportError:
                st.error("umap-learn not installed. Run: pip install umap-learn --break-system-packages")
                st.stop()

        plot_df = df.copy()
        plot_df["x"] = coords[:, 0]
        plot_df["y"] = coords[:, 1]
        if dims == 3:
            plot_df["z"] = coords[:, 2]
        plot_df["preview"] = plot_df["document"].str.slice(0, 80)

        color_arg = None if color_field == "(none)" else color_field
        if dims == 2:
            fig = px.scatter(plot_df, x="x", y="y", color=color_arg,
                              hover_data={"preview": True, "id": True},
                              title=f"{method} projection ({len(plot_df)} points)")
        else:
            fig = px.scatter_3d(plot_df, x="x", y="y", z="z", color=color_arg,
                                 hover_data={"preview": True, "id": True},
                                 title=f"{method} projection ({len(plot_df)} points)")
        fig.update_layout(height=650)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Hover a point to read the chunk. Click-drag to rotate (3D) or zoom (2D).")

# ---------------------------------------------------------------------------
# TAB 4: Cluster drill-down
# ---------------------------------------------------------------------------
with tab_cluster:
    st.subheader("KMeans clustering + drill-down")
    if embeddings is None or len(embeddings) == 0:
        st.warning("This collection has no stored embeddings to cluster.")
    else:
        n_clusters = st.slider("Number of clusters (k)", 2, min(15, len(embeddings)), 4)
        from sklearn.decomposition import PCA
        from sklearn.cluster import KMeans

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10).fit(embeddings)
        cluster_ids = kmeans.labels_
        coords = PCA(n_components=2).fit_transform(embeddings)

        plot_df = df.copy()
        plot_df["x"] = coords[:, 0]
        plot_df["y"] = coords[:, 1]
        plot_df["cluster"] = cluster_ids.astype(str)
        plot_df["preview"] = plot_df["document"].str.slice(0, 80)

        fig = px.scatter(plot_df, x="x", y="y", color="cluster",
                          hover_data={"preview": True, "id": True},
                          title=f"KMeans clusters (k={n_clusters}) over PCA projection")
        fig.update_layout(height=550)
        st.plotly_chart(fig, use_container_width=True)

        chosen_cluster = st.selectbox("Drill into cluster", sorted(set(cluster_ids)))
        cluster_docs = plot_df[plot_df["cluster"] == str(chosen_cluster)]
        st.write(f"**{len(cluster_docs)} items in cluster {chosen_cluster}:**")
        st.dataframe(cluster_docs[["id", "document"]], use_container_width=True, height=350)
