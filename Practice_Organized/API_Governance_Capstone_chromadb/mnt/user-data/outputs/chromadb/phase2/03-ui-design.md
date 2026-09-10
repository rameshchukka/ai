# UI Design — Phase 2 Additions
## Mule API Semantic Detection & Composition Phase

**Screens added in Phase 2:** 3 new + 1 updated
**Phase 1 screens unchanged:** Graph Explorer, Findings Dashboard

---

## Navigation update

```
app/
├── 1_Graph_Explorer.py          Phase 1 — unchanged
├── 2_Findings_Dashboard.py      Phase 1 — unchanged
├── 3_Merge_Impact.py            Phase 1 — updated (llm_rationale now visible)
├── 4_API_Discovery.py           NEW
├── 5_Composition_Advisor.py     NEW
└── 6_Embedding_Health.py        NEW
```

---

## Screen 3 update — Merge Candidates & Impact Analysis

Only change: `llm_rationale` column now populated. Remove the "pending"
placeholder and display the actual rationale text. Also add `semantic_score`
metric alongside the existing `structural_score`.

```python
# Updated card metrics in app/3_Merge_Impact.py
m1, m2, m3, m4 = st.columns(4)
m1.metric("Structural", f"{c['structural_score']:.2f}")
m2.metric("Semantic",   f"{c['semantic_score']:.2f}"
          if c['semantic_score'] else "pending")
m3.metric("Domain",     "Same" if same_domain else "Different")
m4.markdown(f"Risk: :{risk_col}[**{c['traffic_risk'] or 'UNKNOWN'}**]")

# LLM rationale — now populated
if c['llm_rationale']:
    with st.expander("LLM rationale"):
        st.write(c['llm_rationale'])
```

---

## Screen 4 — API Discovery

### Purpose
Fast developer search — find an existing API before building anything.
Three search modes auto-detected from what the developer types.

### Layout

```
+----------------------------------------------------------------+
|  API Discovery                                                  |
|  Find existing APIs before building something new               |
|                                                                  |
|  [Search by purpose, field name, or domain...       ]  [Clear] |
|                                                                  |
|  Layer: [All v]   Domain: [All v]                               |
|  ----------------------------------------------------------------|
|                                                                  |
|  5 APIs found   mode: semantic                                   |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |  proc-nach-debit-api                         [PROC] payments|  |
|  |  NACH Debit Processing                                      |  |
|  |  Orchestrates NACH debit - validates mandate...             |  |
|  |  Endpoint: /proc/v1/nach/debit/initiate                    |  |
|  |  Owner: payments-team                                       |  |
|  |  Relevance: ########..  82%  [v YES - This API processes...]|  |
|  |                                        [View detail ->]     |  |
|  +------------------------------------------------------------+  |
```

### Three search modes

```python
import re

def detect_mode(query: str) -> str:
    q = query.strip()
    # snake_case -> field search
    if re.match(r'^[a-z][a-z0-9]*(_[a-z0-9]+)+$', q):
        return 'field'
    return 'semantic'   # taxonomy check happens after DB lookup

def search_apis(query: str, conn, filters: dict = None) -> list[dict]:
    mode    = detect_mode(query)
    results = {}

    if mode == 'field':
        for r in run_field_search(query, conn):
            results[r['node_id']] = {**r, 'relevance': 0.90, 'match_type': 'field'}
    else:
        # Check taxonomy first
        tax_results = run_taxonomy_search(query, conn)
        if tax_results:
            for r in tax_results:
                results[r['node_id']] = {**r, 'relevance': 0.85, 'match_type': 'taxonomy'}
        else:
            # Semantic - expand query first via LLM
            variants = expand_query(query)
            for variant in variants:
                vec = get_embedding(variant)
                for r in run_semantic_search(vec, conn, filters):
                    nid = r['node_id']
                    if nid not in results or r['relevance_score'] > results[nid]['relevance']:
                        results[nid] = {**r, 'relevance': r['relevance_score'],
                                        'match_type': 'semantic'}

    # Apply filters
    if filters:
        if filters.get('layer'):
            results = {k: v for k, v in results.items()
                       if v.get('layer') == filters['layer']}
        if filters.get('domain'):
            results = {k: v for k, v in results.items()
                       if v.get('domain') == filters['domain']}

    return sorted(results.values(), key=lambda x: x['relevance'], reverse=True)
```

### SQL per mode

```python
def run_semantic_search(query_vec, conn, filters=None) -> list[dict]:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(\"\"\"
            SELECT n.node_id, n.project_name, n.layer,
                   dt.domain_name AS domain, n.functionality,
                   n.listener_endpoint, n.purpose_text, n.owning_team,
                   1 - (e.embedding <=> %s::vector) AS relevance_score
            FROM node_embeddings e
            JOIN api_nodes n ON n.node_id = e.node_id
            LEFT JOIN domain_taxonomy dt ON dt.domain_id = n.domain_id
            WHERE e.chunk_type = 'purpose'
              AND n.status = 'active'
              AND 1 - (e.embedding <=> %s::vector) >= 0.50
            ORDER BY e.embedding <=> %s::vector
            LIMIT 20
        \"\"\", (query_vec, query_vec, query_vec))
        return cur.fetchall()

def run_field_search(field_name: str, conn) -> list[dict]:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(\"\"\"
            SELECT DISTINCT ON (n.node_id)
                n.node_id, n.project_name, n.layer,
                dt.domain_name AS domain, n.functionality,
                n.listener_endpoint, n.purpose_text, n.owning_team,
                f.direction, f.field_name, f.data_type
            FROM api_fields f
            JOIN api_nodes n ON n.node_id = f.node_id
            LEFT JOIN domain_taxonomy dt ON dt.domain_id = n.domain_id
            WHERE n.status = 'active'
              AND (f.field_name = %s OR f.field_name ILIKE '%%'||%s||'%%')
            ORDER BY n.node_id,
                CASE WHEN f.field_name = %s THEN 0 ELSE 1 END
        \"\"\", (field_name, field_name, field_name))
        return cur.fetchall()

def run_taxonomy_search(query: str, conn) -> list[dict]:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(\"\"\"
            SELECT n.node_id, n.project_name, n.layer,
                   dt.domain_name AS domain, ft.functionality_name AS functionality,
                   n.listener_endpoint, n.purpose_text, n.owning_team
            FROM api_nodes n
            LEFT JOIN domain_taxonomy dt ON dt.domain_id = n.domain_id
            LEFT JOIN functionality_taxonomy ft ON ft.functionality_id = n.functionality_id
            WHERE n.status = 'active'
              AND (dt.domain_name ILIKE '%%'||%s||'%%'
                   OR ft.functionality_name ILIKE '%%'||%s||'%%')
            ORDER BY n.layer, n.project_name
        \"\"\", (query, query))
        return cur.fetchall()
```

### Streamlit implementation

```python
# app/4_API_Discovery.py
import streamlit as st
import threading
from core import search, llm, db

st.title("API Discovery")
st.caption("Find existing APIs before building something new")

query = st.text_input("", placeholder="Try: 'mandate debit', 'mandate_id', 'payments'")
c1, c2 = st.columns(2)
layer_f  = c1.selectbox("Layer",  ["All","exp","proc","sys"])
domain_f = c2.selectbox("Domain", ["All"] + search.get_all_domains(db.get_conn()))

if query and len(query.strip()) >= 2:
    filters = {}
    if layer_f  != "All": filters['layer']  = layer_f
    if domain_f != "All": filters['domain'] = domain_f

    with st.spinner("Searching..."):
        conn    = db.get_conn()
        results = search.search_apis(query.strip(), conn, filters)

    st.caption(f"{len(results)} APIs found")

    if not results:
        st.info("No match found. Try the Composition Advisor for a full analysis.")
    else:
        placeholders = {}
        for r in results:
            with st.container(border=True):
                h1, h2 = st.columns([5,1])
                h1.subheader(r['project_name'])
                layer_col = {"exp":"blue","proc":"orange","sys":"green"}.get(r.get('layer',''),"gray")
                h2.markdown(f":{layer_col}[**{(r.get('layer') or '').upper()}**]")
                st.caption(f"{r.get('functionality','—')}  ·  {r.get('domain','—')}  ·  {r.get('owning_team','—')}")
                st.write(r.get('purpose_text','')[:120])
                if r.get('listener_endpoint'):
                    st.code(r['listener_endpoint'], language=None)
                rc, ac = st.columns([3,1])
                rc.progress(float(r.get('relevance',0)),
                            text=f"Relevance: {float(r.get('relevance',0)):.0%}  ({r.get('match_type','')})")
                if ac.button("View detail", key=f"d_{r['node_id']}"):
                    st.session_state['filter_node'] = r['node_id']
                    st.switch_page("pages/1_Graph_Explorer.py")
                placeholders[r['node_id']] = st.empty()

        # Async LLM quick-takes
        def run_quick_takes():
            takes = llm.quick_take_batch(query, results, db.get_conn())
            for t in takes:
                ph = placeholders.get(t['node_id'])
                if ph:
                    col = {"YES":"green","PARTIAL":"orange","NO":"red"}[t['verdict']]
                    ph.markdown(f":{col}[**{t['verdict']}** — {t['note']}]")

        threading.Thread(target=run_quick_takes, daemon=True).start()
```

---

## Screen 5 — Composition Advisor

### Purpose
Formal analysis for a new requirement — DIRECT_MATCH / COMPOSE / NEW_BUILD
with LLM rationale and field mapping detail.

### Layout

```
+----------------------------------------------------------------+
|  Composition Advisor                                            |
|  "Does an existing API satisfy this new requirement?"           |
|                                                                  |
|  [Describe your requirement in plain English          ]         |
|  [Analyze]                                                       |
|  ----------------------------------------------------------------|
|  Processing: embedding -> retrieval -> scoring -> LLM decision  |
|  ----------------------------------------------------------------|
|                                                                  |
|  [DIRECT_MATCH]  Confidence: HIGH                               |
|  proc-nach-debit-api                                             |
|  Similarity: 0.87   Schema: 1.00   Domain: 1.00                 |
|  Score: 0.94                                                     |
|                                                                  |
|  LLM rationale:                                                  |
|  This API directly satisfies the requirement. It accepts         |
|  mandate_id, debit amount and bank details, and submits to       |
|  the NACH clearance system.                                      |
|                                                                  |
|  Comment: _______________________________________________        |
|  [Approve]  [Reject]                                             |
+----------------------------------------------------------------+
```

### Implementation

```python
# app/5_Composition_Advisor.py
import streamlit as st, json
from core import composition, db

st.title("Composition Advisor")
st.caption("Does an existing API satisfy this new requirement?")

requirement = st.text_area("New requirement", height=100,
    placeholder="e.g. Process a NACH mandate debit for recurring payment collection")

if st.button("Analyze") and requirement.strip():
    conn = db.get_conn()

    with st.spinner("Embedding requirement..."):
        candidates = composition.analyze_requirement(requirement, conn)

    if not candidates:
        st.warning("No candidates found — this appears to be a NEW_BUILD requirement.")
    else:
        for c in candidates[:3]:
            band = c.get('recommendation', 'NEW_BUILD')
            band_col = {"DIRECT_MATCH":"green","COMPOSE":"orange","NEW_BUILD":"red"}[band]
            with st.container(border=True):
                st.markdown(f":{band_col}[**{band}**]  Confidence: {c.get('confidence','—')}")
                st.subheader("  +  ".join(c.get('nodes', [])))
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Similarity",  f"{c.get('similarity',0):.2f}")
                m2.metric("Schema",      f"{c.get('schema_compat',0):.2f}")
                m3.metric("Domain",      f"{c.get('domain_align',0):.2f}")
                m4.metric("Score",       f"{c.get('score',0):.2f}")

                if c.get('rationale'):
                    st.info(c['rationale'])

                if c.get('risks'):
                    st.warning(f"Risk: {c['risks']}")

                # Field mapping table (for COMPOSE)
                if band == 'COMPOSE' and c.get('field_mappings'):
                    with st.expander("Field mapping detail"):
                        fm_data = [{"target field": m['target_field']['field_name'],
                                    "required": m['target_field']['is_required'],
                                    "satisfied": m['satisfied'],
                                    "match type": m.get('match',{}).get('match_type','—'),
                                    "confidence": m.get('match',{}).get('confidence',0)}
                                   for m in c['field_mappings']]
                        st.dataframe(fm_data, use_container_width=True)

                comment = st.text_input("Comment (required)", key=f"cmt_{c.get('composition_id','')}")
                b1, b2 = st.columns(2)
                if b1.button("Approve", key=f"apr_{c.get('composition_id','')}"):
                    if comment:
                        with conn:
                            with conn.cursor() as cur:
                                cur.execute("UPDATE composition_candidates SET status='approved' WHERE composition_id=%s",
                                            (c.get('composition_id'),))
                                cur.execute("INSERT INTO audit_log (entity_type,entity_id,action,comment,reviewer) VALUES ('composition_candidate',%s,'approved',%s,'architect')",
                                            (c.get('composition_id'), comment))
                        st.success("Approved and recorded.")
                        st.rerun()
                    else:
                        st.warning("Comment required")
```

---

## Screen 6 — Embedding Health

### Purpose
Confirms that vector embeddings separate correctly by domain.
Run after any bulk ingestion of new APIs.

### Layout

```
+----------------------------------------------------------------+
|  Embedding Health                                               |
|                                                                  |
|  Chunk type: [purpose v]                                        |
|                                                                  |
|  UMAP scatter plot                                              |
|  [                    plot renders here                     ]   |
|                                                                  |
|  Separation metrics                                             |
|  Within-domain similarity : 0.284                               |
|  Cross-domain similarity  : 0.142                               |
|  Gap (want > 0.10)        : 0.142    [v OK]                    |
|                                                                  |
|  Coverage                                                        |
|  Nodes with purpose embedding : 700 / 700                       |
|  Nodes missing any embedding  : 0                               |
+----------------------------------------------------------------+
```

### Implementation

```python
# app/6_Embedding_Health.py
import streamlit as st
import numpy as np, matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from core import db

st.title("Embedding Health")

chunk_type = st.selectbox("Chunk type",
    ["purpose","business_rules","request_fields","response_fields"])

conn = db.get_conn()
with conn.cursor() as cur:
    cur.execute(\"\"\"
        SELECT e.embedding, dt.domain_name, n.project_name
        FROM node_embeddings e
        JOIN api_nodes n ON n.node_id = e.node_id
        LEFT JOIN domain_taxonomy dt ON dt.domain_id = n.domain_id
        WHERE e.chunk_type = %s AND n.status = 'active'
    \"\"\", (chunk_type,))
    rows = cur.fetchall()

if not rows:
    st.warning(f"No embeddings found for chunk_type='{chunk_type}'")
else:
    embeddings = np.array([r[0] for r in rows])
    domains    = [r[1] or 'unknown' for r in rows]

    # Numeric gap
    sim = cosine_similarity(embeddings)
    within, across = [], []
    for i in range(len(domains)):
        for j in range(i+1, len(domains)):
            (within if domains[i]==domains[j] else across).append(sim[i][j])
    gap = np.mean(within) - np.mean(across)

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Within-domain similarity", f"{np.mean(within):.3f}")
    c2.metric("Cross-domain similarity",  f"{np.mean(across):.3f}")
    c3.metric("Gap (want > 0.10)",
              f"{gap:.3f}",
              delta="OK" if gap > 0.10 else "LOW")

    # UMAP plot
    try:
        import umap
        reducer   = umap.UMAP(n_neighbors=min(15,len(rows)-1),
                               min_dist=0.1, metric='cosine', random_state=42)
        projected = reducer.fit_transform(embeddings)
        unique_d  = sorted(set(domains))
        colors    = plt.cm.tab10(np.linspace(0,1,len(unique_d)))
        cmap      = dict(zip(unique_d, colors))
        fig, ax   = plt.subplots(figsize=(9,6))
        for d in unique_d:
            idx = [i for i,dom in enumerate(domains) if dom==d]
            ax.scatter(projected[idx,0], projected[idx,1],
                       label=d, color=cmap[d], s=50, alpha=0.8)
        ax.legend(loc='upper right', fontsize=8)
        ax.set_title(f'UMAP — {chunk_type} embeddings (gap={gap:.3f})')
        st.pyplot(fig)
    except ImportError:
        st.info("Install umap-learn for the UMAP plot: pip install umap-learn")

    # Coverage
    st.subheader("Coverage")
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM api_nodes WHERE status='active'")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT node_id) FROM node_embeddings WHERE chunk_type='purpose'")
        covered = cur.fetchone()[0]
    st.metric("Nodes with purpose embedding", f"{covered} / {total}")
    if covered < total:
        with conn.cursor() as cur:
            cur.execute(\"\"\"
                SELECT n.project_name FROM api_nodes n
                LEFT JOIN node_embeddings e
                       ON e.node_id=n.node_id AND e.chunk_type='purpose'
                WHERE n.status='active' AND e.embedding_id IS NULL
            \"\"\")
            missing = [r[0] for r in cur.fetchall()]
        st.warning(f"{len(missing)} nodes missing purpose embedding:")
        st.write(missing)
```
