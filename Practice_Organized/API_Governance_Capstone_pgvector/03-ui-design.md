# UI Design
## Mule API Structural Detection Platform — Phase 1

**Screens in this phase:** 3
**Deferred:** API Discovery, Composition Advisor, Embedding Health

---

## Screens overview

| # | Screen | File | Purpose |
|---|---|---|---|
| 1 | Graph Explorer | `app/1_Graph_Explorer.py` | Visual call graph — see all nodes, edges, and finding overlays |
| 2 | Findings Dashboard | `app/2_Findings_Dashboard.py` | Review all structural findings, approve/dismiss with audit trail |
| 3 | Merge Candidates & Impact | `app/3_Merge_Impact.py` | Action duplicate-flow merge proposals, run impact analysis |

Run with: `streamlit run app/1_Graph_Explorer.py`

---

## Screen 1 — Graph Explorer

### Purpose
The entry point to the platform. Shows the complete Mule API call graph
coloured by layer. Structural findings are overlaid as highlights so an
architect can see at a glance where the redundancy is.

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  SIDEBAR                │  GRAPH CANVAS                         │
│                         │                                        │
│  Layer filter           │   [exp node]──►[proc node]──►[sys node]│
│  □ exp  □ proc  □ sys  │                                        │
│                         │   [exp node]──►[proc node]──►[sys node]│
│  Domain filter          │                     ↑                  │
│  [dropdown]             │              (fan-in cluster)          │
│                         │                                        │
│  Finding overlay        │                                        │
│  □ Show findings        │                                        │
│                         │                                        │
│  ─────────────────────  │                                        │
│  NODE DETAIL            │                                        │
│  (populated on click)   │                                        │
│  Name:                  │                                        │
│  Layer:                 │                                        │
│  Domain:                │                                        │
│  Owning team:           │                                        │
│  Endpoint:              │                                        │
│  Open findings: N       │                                        │
│  [View findings →]      │                                        │
└─────────────────────────────────────────────────────────────────┘
```

### Node colours
- 🔵 Blue `#4C72B0` — Exp layer
- 🟠 Orange `#DD8452` — Proc layer
- 🟢 Green `#55A868` — Sys layer

### Node size
Proportional to `in_degree`. A large Sys node = many callers = high fan-in
risk. Used as a visual pre-attentive cue before the architect reads findings.

### Finding overlays (when "Show findings" is checked)
- **Red dashed edges** — part of a DUPLICATE_FLOW finding
- **Red halo on Proc node** — flagged as PASS_THROUGH_HOP
- **Orange path highlight** — part of a DEEP_CHAIN finding
- **Purple ring on Sys node** — FAN_IN_CLUSTER finding

### Behaviour

```python
# core/graph.py
import networkx as nx

def build_graph(conn) -> nx.DiGraph:
    """Build networkx graph from api_nodes and api_edges."""
    G = nx.DiGraph()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(\"\"\"
            SELECT node_id, project_name, layer, domain,
                   functionality, owning_team, listener_endpoint, status
            FROM api_nodes WHERE status = 'active'
        \"\"\")
        for row in cur.fetchall():
            G.add_node(row['node_id'], **row)

        cur.execute(\"\"\"
            SELECT source_node_id, target_node_id,
                   source_endpoint_path, target_endpoint_path
            FROM api_edges
        \"\"\")
        for row in cur.fetchall():
            G.add_edge(row['source_node_id'], row['target_node_id'], **row)
    return G


# app/1_Graph_Explorer.py  (key logic)
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from core import graph, db

conn = db.get_conn()
G    = graph.build_graph(conn)

# Load open findings for overlay
with conn.cursor() as cur:
    cur.execute(\"\"\"
        SELECT finding_id, pattern_type, node_ids, detail
        FROM structural_findings WHERE review_status = 'open'
    \"\"\")
    findings = cur.fetchall()

# Build node_ids in findings for overlay colouring
finding_nodes = set()
for f in findings:
    finding_nodes.update(f[2])  # node_ids array

# Build agraph nodes
nodes, edges = [], []
show_findings = st.sidebar.checkbox("Show findings overlay", value=True)
layer_filter  = st.sidebar.multiselect("Layer", ['exp','proc','sys'],
                                        default=['exp','proc','sys'])
domain_filter = st.sidebar.selectbox("Domain", ["All"] + get_domains(conn))

COLOURS = {'exp': '#4C72B0', 'proc': '#DD8452', 'sys': '#55A868'}
for nid, data in G.nodes(data=True):
    if data['layer'] not in layer_filter:
        continue
    if domain_filter != "All" and data.get('domain') != domain_filter:
        continue
    colour = '#E74C3C' if (show_findings and nid in finding_nodes) else COLOURS[data['layer']]
    size   = 15 + min(G.in_degree(nid) * 5, 35)
    nodes.append(Node(id=str(nid), label=data['project_name'].replace('-api',''),
                      size=size, color=colour))

for src, tgt, data in G.edges(data=True):
    edges.append(Edge(source=str(src), target=str(tgt)))

config = Config(width=900, height=600, directed=True,
                physics=True, hierarchical=False)
selected = agraph(nodes=nodes, edges=edges, config=config)

# Node detail panel
if selected:
    nid  = int(selected)
    data = G.nodes[nid]
    st.sidebar.markdown(f"**{data['project_name']}**")
    st.sidebar.write(f"Layer: `{data['layer'].upper()}`")
    st.sidebar.write(f"Domain: {data.get('domain','—')}")
    st.sidebar.write(f"Team: {data.get('owning_team','—')}")
    st.sidebar.write(f"Endpoint: `{data.get('listener_endpoint','—')}`")
    open_findings = [f for f in findings if nid in f[2]]
    st.sidebar.write(f"Open findings: {len(open_findings)}")
    if open_findings:
        if st.sidebar.button("View findings →"):
            st.session_state['filter_node'] = nid
            st.switch_page("pages/2_Findings_Dashboard.py")
```

---

## Screen 2 — Findings Dashboard

### Purpose
List all structural findings, filter by pattern type or status, and mark
each as reviewed or dismissed with a mandatory comment.

### Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Structural Findings                    [Export CSV]             │
│                                                                   │
│  Pattern:  [ALL ▼]   Status: [open ▼]   Domain: [ALL ▼]        │
│  Run:      [Latest ▼]  Severity: [ALL ▼]                        │
│  ─────────────────────────────────────────────────────────────── │
│                                                                   │
│  [HIGH] DUPLICATE_FLOW   sys-crm-api ← 2 paths   [Review ▼]    │
│  exp-customer-360 → proc-customer-orchestration → sys-crm        │
│  exp-account-summary → proc-account-lookup → sys-crm             │
│  ─────────────────────────────────────────────────────────────── │
│  [MED]  PASS_THROUGH_HOP  proc-order-status has 1 outbound      │
│  exp-order-status → proc-order-status → sys-oms                  │
│  ─────────────────────────────────────────────────────────────── │
│  [LOW]  DEEP_CHAIN  4 hops  exp-claims → ... → sys-policy        │
│  ─────────────────────────────────────────────────────────────── │
│  [LOW]  FAN_IN_CLUSTER  sys-crm ← 3 Proc APIs                   │
│  ─────────────────────────────────────────────────────────────── │
│                                                                   │
│  Showing 4 of 4  |  PASS  0  |  WARN  0  |  FAIL  0            │
└──────────────────────────────────────────────────────────────────┘
```

### Finding card — expanded

```
┌──────────────────────────────────────────────────────────────────┐
│ [HIGH]  DUPLICATE_FLOW          Detected: 2024-02-01  [open]    │
│ ─────────────────────────────────────────────────────────────── │
│ Terminal: sys-crm-api                                            │
│                                                                   │
│ Path A:  exp-customer-360-api                                    │
│          → proc-customer-orchestration-api  (/proc/v1/customer)  │
│          → sys-crm-api  (/crm/v2/customer/lookup)                │
│                                                                   │
│ Path B:  exp-account-summary-api                                 │
│          → proc-account-lookup-api  (/proc/v1/account/lookup)    │
│          → sys-crm-api  (/crm/v2/customer/lookup)                │
│                                                                   │
│ Recommendation: Raise merge candidate for the two Proc APIs      │
│                                                                   │
│ Comment: ___________________________________________________      │
│                                                                   │
│   [Mark reviewed]  [Dismiss]  [View in graph →]                  │
└──────────────────────────────────────────────────────────────────┘
```

### Behaviour

```python
# app/2_Findings_Dashboard.py
import streamlit as st
from core import db
from psycopg2.extras import RealDictCursor

conn = db.get_conn()

# Filters
col1, col2, col3, col4 = st.columns(4)
pattern_filter = col1.selectbox("Pattern", ["ALL","DUPLICATE_FLOW",
    "PASS_THROUGH_HOP","DEEP_CHAIN","FAN_IN_CLUSTER"])
status_filter  = col2.selectbox("Status", ["open","reviewed","dismissed","ALL"])
severity_filter= col3.selectbox("Severity", ["ALL","HIGH","MEDIUM","LOW"])

where_clauses = []
params = []
if pattern_filter != "ALL":
    where_clauses.append("f.pattern_type = %s"); params.append(pattern_filter)
if status_filter != "ALL":
    where_clauses.append("f.review_status = %s"); params.append(status_filter)
if severity_filter != "ALL":
    where_clauses.append("f.severity = %s"); params.append(severity_filter)

where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

with conn.cursor(cursor_factory=RealDictCursor) as cur:
    cur.execute(f\"\"\"
        SELECT f.finding_id, f.pattern_type, f.severity,
               f.node_ids, f.detail, f.detected_at, f.review_status
        FROM structural_findings f
        {where_sql}
        ORDER BY
            CASE f.severity WHEN 'HIGH' THEN 1
                            WHEN 'MEDIUM' THEN 2
                            ELSE 3 END,
            f.detected_at DESC
    \"\"\", params)
    findings = cur.fetchall()

SEVERITY_COLOURS = {'HIGH': 'red', 'MEDIUM': 'orange', 'LOW': 'gray'}

for f in findings:
    col   = SEVERITY_COLOURS.get(f['severity'], 'gray')
    label = f['pattern_type'].replace('_', ' ')
    with st.container(border=True):
        h1, h2 = st.columns([5, 1])
        h1.markdown(f":{col}[**{label}**]  `{f['review_status']}`")
        h2.caption(str(f['detected_at'])[:10])

        detail = f['detail'] or {}
        if f['pattern_type'] == 'DUPLICATE_FLOW':
            st.caption(f"Terminal: **{detail.get('terminal_node')}**")
            st.text(" → ".join(detail.get('flow_a', [])))
            st.text(" → ".join(detail.get('flow_b', [])))
        elif f['pattern_type'] == 'PASS_THROUGH_HOP':
            st.caption(f"{detail.get('proc_node')} has 1 outbound edge → {detail.get('only_calls')}")
        elif f['pattern_type'] == 'DEEP_CHAIN':
            st.caption(f"{detail.get('hop_count')} hops: " + " → ".join(detail.get('path', [])))
        elif f['pattern_type'] == 'FAN_IN_CLUSTER':
            st.caption(f"{detail.get('sys_node')} ← {detail.get('in_degree')} Proc APIs")

        if f['review_status'] == 'open':
            comment = st.text_input("Comment (required)", key=f"cmt_{f['finding_id']}")
            a1, a2, a3 = st.columns(3)
            if a1.button("Mark reviewed", key=f"rev_{f['finding_id']}"):
                if comment:
                    with conn:
                        with conn.cursor() as cur:
                            cur.execute("UPDATE structural_findings SET review_status='reviewed' WHERE finding_id=%s", (f['finding_id'],))
                            cur.execute("INSERT INTO audit_log (entity_type,entity_id,action,comment,reviewer) VALUES ('finding',%s,'reviewed',%s,'architect')", (f['finding_id'], comment))
                    st.rerun()
                else:
                    st.warning("Comment required")
            if a2.button("Dismiss", key=f"dis_{f['finding_id']}"):
                if comment:
                    with conn:
                        with conn.cursor() as cur:
                            cur.execute("UPDATE structural_findings SET review_status='dismissed' WHERE finding_id=%s", (f['finding_id'],))
                            cur.execute("INSERT INTO audit_log (entity_type,entity_id,action,comment,reviewer) VALUES ('finding',%s,'dismissed',%s,'architect')", (f['finding_id'], comment))
                    st.rerun()
                else:
                    st.warning("Comment required")
```

---

## Screen 3 — Merge Candidates & Impact Analysis

### Purpose
Two panels in one screen:
- **Left / top:** merge candidate cards for DUPLICATE_FLOW pairs — approve,
  reject, or defer. Structural score shown; LLM rationale added in next phase.
- **Right / bottom:** impact analysis tree — upstream and downstream for any
  API the architect searches.

### Layout

```
┌──────────────────────────────────┬───────────────────────────────┐
│  MERGE CANDIDATES                │  IMPACT ANALYSIS              │
│                                  │                               │
│  proc-customer-orchestration     │  Search: [_______________]    │
│  ↔  proc-account-lookup          │                               │
│  ──────────────────────────────  │  ⬆ Upstream callers:          │
│  Structural score: 0.88          │    exp-customer-360           │
│  Domain alignment: ✓ same        │    exp-account-summary        │
│  Traffic risk: LOW               │                               │
│  LLM rationale: pending          │  ⬇ Downstream callees:        │
│                                  │    sys-crm-api                │
│  Comment: _________________      │      /crm/v2/customer/lookup  │
│  [Approve] [Reject] [Defer]      │                               │
│                                  │  Hop depth: 2                 │
│  ─────────────────────────────── │                               │
│  (next candidate...)             │                               │
└──────────────────────────────────┴───────────────────────────────┘
```

### Merge candidate card — detail

```python
# app/3_Merge_Impact.py  — merge candidates section
import streamlit as st
from core import db
from psycopg2.extras import RealDictCursor

conn = db.get_conn()
left, right = st.columns([1, 1])

with left:
    st.subheader("Merge Candidates")
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(\"\"\"
            SELECT mc.candidate_id, mc.structural_score,
                   mc.traffic_risk, mc.recommendation,
                   mc.confidence, mc.llm_rationale, mc.status,
                   na.project_name AS name_a,
                   nb.project_name AS name_b,
                   da.domain_name  AS domain_a,
                   db2.domain_name AS domain_b
            FROM merge_candidates mc
            JOIN api_nodes na ON na.node_id = mc.node_a_id
            JOIN api_nodes nb ON nb.node_id = mc.node_b_id
            LEFT JOIN domain_taxonomy da ON da.domain_id = na.domain_id
            LEFT JOIN domain_taxonomy db2 ON db2.domain_id = nb.domain_id
            WHERE mc.status = 'pending'
            ORDER BY mc.structural_score DESC
        \"\"\")
        candidates = cur.fetchall()

    for c in candidates:
        same_domain = c['domain_a'] == c['domain_b']
        with st.container(border=True):
            st.markdown(f"**{c['name_a']}**  ↔  **{c['name_b']}**")
            m1, m2, m3 = st.columns(3)
            m1.metric("Structural score", f"{c['structural_score']:.2f}")
            m2.metric("Domain", "✓ Same" if same_domain else "✗ Different")
            risk_col = "red" if c['traffic_risk']=='HIGH' else "orange" if c['traffic_risk']=='MEDIUM' else "green"
            m3.markdown(f"Traffic risk: :{risk_col}[**{c['traffic_risk'] or 'UNKNOWN'}**]")

            if c['llm_rationale']:
                with st.expander("LLM rationale"):
                    st.write(c['llm_rationale'])
            else:
                st.caption("_LLM rationale: pending (added in semantic detection phase)_")

            comment = st.text_input("Comment (required)",
                                     key=f"mc_cmt_{c['candidate_id']}")
            b1, b2, b3 = st.columns(3)
            for action, col in [('approved', b1), ('rejected', b2), ('deferred', b3)]:
                if col.button(action.capitalize(), key=f"mc_{action}_{c['candidate_id']}"):
                    if comment:
                        with conn:
                            with conn.cursor() as cur:
                                cur.execute("UPDATE merge_candidates SET status=%s WHERE candidate_id=%s",
                                            (action, c['candidate_id']))
                                cur.execute("INSERT INTO audit_log (entity_type,entity_id,action,comment,reviewer) VALUES ('merge_candidate',%s,%s,%s,'architect')",
                                            (c['candidate_id'], action, comment))
                        st.rerun()
                    else:
                        st.warning("Comment required")

# ── Impact Analysis ─────────────────────────────────────────────────────────
with right:
    st.subheader("Impact Analysis")
    search = st.text_input("API project name or endpoint",
                            placeholder="proc-nach-debit-api")
    if search:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(\"\"\"
                SELECT node_id, project_name, layer
                FROM api_nodes
                WHERE project_name ILIKE %s AND status='active'
                LIMIT 1
            \"\"\", (f'%{search}%',))
            target = cur.fetchone()

        if not target:
            st.warning("API not found")
        else:
            nid = target['node_id']
            st.caption(f"**{target['project_name']}** [{target['layer'].upper()}]")

            # Upstream (who calls this)
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(\"\"\"
                    SELECT n.project_name, n.layer,
                           e.source_endpoint_path, e.target_endpoint_path
                    FROM api_edges e
                    JOIN api_nodes n ON n.node_id = e.source_node_id
                    WHERE e.target_node_id = %s AND n.status='active'
                    ORDER BY n.layer, n.project_name
                \"\"\", (nid,))
                upstream = cur.fetchall()

            st.markdown("**⬆ Upstream — APIs that call this:**")
            if upstream:
                for u in upstream:
                    st.markdown(f"  `{u['layer'].upper()}`  {u['project_name']}")
                    st.caption(f"  &nbsp;&nbsp;&nbsp; via `{u['source_endpoint_path']} → {u['target_endpoint_path']}`")
            else:
                st.caption("None — this is an entry point")

            # Downstream (what this calls)
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(\"\"\"
                    SELECT n.project_name, n.layer,
                           e.source_endpoint_path, e.target_endpoint_path
                    FROM api_edges e
                    JOIN api_nodes n ON n.node_id = e.target_node_id
                    WHERE e.source_node_id = %s AND n.status='active'
                    ORDER BY n.layer, n.project_name
                \"\"\", (nid,))
                downstream = cur.fetchall()

            st.markdown("**⬇ Downstream — APIs this calls:**")
            if downstream:
                for d in downstream:
                    st.markdown(f"  `{d['layer'].upper()}`  {d['project_name']}")
                    st.caption(f"  &nbsp;&nbsp;&nbsp; via `{d['source_endpoint_path']} → {d['target_endpoint_path']}`")
            else:
                st.caption("None — this is a terminal node")
```

---

## Navigation

```
app/
├── 1_Graph_Explorer.py       ← default landing page
├── 2_Findings_Dashboard.py
└── 3_Merge_Impact.py
```

Streamlit's built-in multi-page navigation generates the sidebar automatically
from the file names. `st.switch_page()` links between screens (e.g. "View in graph"
from the Findings Dashboard jumps to Graph Explorer with that node selected).
