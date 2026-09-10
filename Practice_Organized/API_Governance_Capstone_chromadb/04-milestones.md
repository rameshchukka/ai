# Milestones
## Mule API Structural Detection Platform — Phase 1

**7 milestones. Complete in order. Never start the next until the verify
check passes.**

---

## Milestone map

| # | Name | Depends on | Delivers |
|---|---|---|---|
| M1 | Schema & Data Load | — | All 19 tables created, sample data in api_nodes + api_edges |
| M1b | Taxonomy Seeding & Version Detection | M1 | domain_taxonomy populated, api_versions linked |
| M2 | Traversal & Structural Detection | M1b | flows built, all 4 pattern findings in structural_findings |
| M7 | Core Module Assembly | M2 | Clean core/ package: db, graph, traversal, rules |
| M8 | Streamlit: Graph Explorer & Findings Dashboard | M7 | Screens 1 and 2 live |
| M10 | Streamlit: Merge Candidates & Impact Analysis | M7 | Screen 3 live |
| M12 | Refresh, Snapshots & Audit Trail | M8, M10 | Weekly refresh, edge_history, finding diff |

---

## M1 — Schema & Data Load

**Goal:** All 19 PostgreSQL tables created. Sample data loaded into
`api_nodes` and `api_edges`. All table counts verified before moving on.
The reserved tables (node_embeddings, api_fields, etc.) are created now so
no migration is needed later — they just stay empty.

**Agent prompt:**
```
Create all 19 PostgreSQL tables from the DDL in 01-srs.md Sections 2.1–2.21,
including CREATE EXTENSION IF NOT EXISTS vector for the node_embeddings table.
Write a Python loader that reads the sample JSON from 06-data-ingestion-guide.md
Section 2 and inserts into api_nodes and api_edges.

Validation rules:
- Reject any node where layer is not in ('exp','proc','sys')
- Reject any edge where source or target project_name does not exist in api_nodes
- Print per-table row counts after loading — even reserved tables should show 0

Also insert one ingestion_runs row for this load and populate source_repos
(one row per API in the sample).
```

**Verify:**
```sql
-- All 19 tables must exist
SELECT COUNT(*) FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
-- Expected: 19 (includes reserved tables at 0 rows)

-- Nodes and edges loaded
SELECT COUNT(*) FROM api_nodes WHERE status = 'active';
SELECT COUNT(*) FROM api_edges;

-- No nodes with NULL domain (will be fixed in M1b but should not be blank from source)
SELECT project_name FROM api_nodes WHERE domain IS NULL;

-- Ingestion run recorded
SELECT run_id, status, nodes_created, edges_created
FROM ingestion_runs ORDER BY started_at DESC LIMIT 1;
```

---

## M1b — Taxonomy Seeding & Version Detection

**Goal:** `domain_taxonomy` populated with canonical domain names.
`api_nodes.domain_id` fully mapped — no nulls. `api_versions` populated
for any APIs with version suffixes in their project_name.

**Agent prompt:**
```
Seed domain_taxonomy from the distinct domain values already in api_nodes.
Treat case variants and obvious singular/plural differences (payments vs
Payments vs payment) as one canonical entry — flag genuinely ambiguous cases
for human confirmation rather than guessing.

Update api_nodes.domain_id via foreign key for every row.

Scan all project_names for version indicators: -v1, -v2, -v3, or date-based
suffixes like -2024-03. For each detected version pair, insert into api_versions
linking them to a shared lineage. Where version detection is ambiguous (e.g.
a name ends in -v2 but no -v1 exists), flag it in output rather than guessing.

Print: domains seeded, domain_id nulls remaining, api_versions rows created.
```

**Verify:**
```sql
-- Domain taxonomy populated
SELECT domain_name FROM domain_taxonomy ORDER BY domain_name;

-- CRITICAL: zero nodes without domain_id before M2 runs
-- M2's duplicate-flow rule uses domain for alignment scoring
SELECT project_name FROM api_nodes WHERE domain_id IS NULL AND status = 'active';
-- Must return 0 rows

-- Version detection
SELECT n.project_name, av.version_label, av.is_current
FROM api_versions av
JOIN api_nodes n ON n.node_id = av.node_id
ORDER BY n.project_name;
```

---

## M2 — Traversal & Structural Detection

**Goal:** `flows` table populated with all materialised paths.
`structural_findings` populated with all four pattern types.
`merge_candidates` populated for DUPLICATE_FLOW pairs with structural score.

**Agent prompt:**
```
Implement the recursive CTE from 01-srs.md Section 4 wrapped in a Python
function materialize_flows(conn) that inserts results into the flows table.

Then implement all four detection functions from 01-srs.md Section 5 exactly
as specified:
- find_duplicate_flows: groups flows by terminal_sys_id, finds pairs of
  distinct root Exp nodes reaching the same terminal, checks api_versions
  to suppress version pairs, writes DUPLICATE_FLOW findings
- find_pass_through_hops: finds Proc nodes with out_degree == 1
- find_deep_chains: finds flows with hop_count >= DEEP_CHAIN_THRESHOLD (4)
- find_fan_in_clusters: finds Sys nodes with >= FAN_IN_THRESHOLD (3)
  Proc callers

For every DUPLICATE_FLOW finding, also create a merge_candidates row using
the structural_score() formula from Section 5.5. Set semantic_score and
llm_rationale to NULL — these are added in the semantic detection phase.

Write all findings to structural_findings. Print finding counts per pattern.
```

**Verify:**
```sql
-- Flows built
SELECT COUNT(*) FROM flows;
-- Must be > 0. If 0, check that api_edges has rows and that Exp nodes exist.

-- All four patterns found (for sample data)
SELECT pattern_type, severity, COUNT(*) AS count
FROM structural_findings
GROUP BY pattern_type, severity
ORDER BY count DESC;

-- Duplicate flows have merge candidates
SELECT sf.pattern_type, mc.candidate_id, mc.structural_score,
       na.project_name AS api_a, nb.project_name AS api_b
FROM structural_findings sf
JOIN merge_candidates mc ON mc.candidate_id = (
    SELECT candidate_id FROM merge_candidates
    WHERE ARRAY[node_a_id, node_b_id] && sf.node_ids
    LIMIT 1
)
JOIN api_nodes na ON na.node_id = mc.node_a_id
JOIN api_nodes nb ON nb.node_id = mc.node_b_id
WHERE sf.pattern_type = 'DUPLICATE_FLOW';

-- Version check working: these project names should NOT appear together
-- as a DUPLICATE_FLOW finding (they are versions of the same API)
-- Replace with real version-pair names from your data
SELECT f.finding_id, f.detail
FROM structural_findings f
WHERE f.pattern_type = 'DUPLICATE_FLOW'
  AND f.detail::text LIKE '%v1%' AND f.detail::text LIKE '%v2%';
-- Should return 0 rows if version detection is working
```

---

## M7 — Core Module Assembly

**Goal:** All logic built in M1–M2 reorganised into the clean `core/`
package structure. No logic changes — pure reorganisation with type hints.

**Agent prompt:**
```
Reorganise all functions built in M1, M1b, and M2 into this exact structure:

core/db.py          — get_conn(), connection pooling
core/graph.py       — build_graph(conn) -> nx.DiGraph, get_node_names(conn)
core/traversal.py   — materialize_flows(conn), get_flows_df(conn)
core/rules.py       — find_duplicate_flows, find_pass_through_hops,
                       find_deep_chains, find_fan_in_clusters,
                       run_all_rules(conn) -> list of finding dicts,
                       write_findings(findings, conn),
                       structural_score(flow_a_len, flow_b_len, same_domain)

Do not change any logic — only move code and update imports.
Add Python type hints to all public function signatures.
Add a docstring to each public function.
```

**Verify:**
```python
# Run this Python snippet to confirm the package works correctly
from core.db import get_conn
from core.graph import build_graph
from core.traversal import materialize_flows, get_flows_df
from core.rules import run_all_rules, write_findings

conn     = get_conn()
G        = build_graph(conn)
flows_df = get_flows_df(conn)
findings = run_all_rules(conn)

print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
print(f"Flows: {len(flows_df)} materialised paths")
print(f"Findings: {len(findings)} total")
for f in findings:
    print(f"  {f['pattern_type']} — {len(f['node_ids'])} nodes involved")
```
All four findings counts must match the M2 verify output exactly.

---

## M8 — Streamlit: Graph Explorer & Findings Dashboard

**Goal:** Screens 1 and 2 live. Findings visible in the graph with colour
overlays. Approve/dismiss workflow writing to `audit_log`.

**Agent prompt:**
```
Build app/1_Graph_Explorer.py and app/2_Findings_Dashboard.py exactly as
specified in 03-ui-design.md Sections 1 and 2.

Key requirements:
- Layer colours: exp=#4C72B0, proc=#DD8452, sys=#55A868
- Node size proportional to in_degree (base 15, +5 per caller, max +35)
- Finding overlay: nodes involved in open findings shown in red #E74C3C
  when "Show findings" checkbox is checked
- Findings Dashboard: all four pattern types, severity sort (HIGH first),
  filtered by pattern/status/severity dropdowns
- Mark reviewed and Dismiss buttons: BOTH the status update AND the
  audit_log insert must be in a single transaction (with conn: with cur:)
- Comment is required for both actions — show st.warning if empty
- "View in graph" button passes selected node_id to Graph Explorer via
  st.session_state and st.switch_page

Use streamlit-agraph for graph rendering.
Call core/ functions directly — no HTTP calls.
```

**Verify:**
- Open the app: `streamlit run app/1_Graph_Explorer.py`
- Node count on graph matches `SELECT COUNT(*) FROM api_nodes WHERE status='active'`
- Finding count on dashboard matches `SELECT COUNT(*) FROM structural_findings WHERE review_status='open'`
- Approve one finding → confirm `review_status` updated AND `audit_log` row exists
- "View in graph" → lands on Graph Explorer with correct node selected
- Try approving without a comment → must show warning, not write to DB

---

## M10 — Streamlit: Merge Candidates & Impact Analysis

**Goal:** Screen 3 live. Merge candidates visible with structural score.
Impact analysis upstream/downstream tree working from project name search.

**Agent prompt:**
```
Build app/3_Merge_Impact.py exactly as specified in 03-ui-design.md Section 3.

Merge candidates panel:
- Show only status='pending' candidates, sorted by structural_score DESC
- Display structural_score, domain alignment (same domain = green tick),
  traffic_risk from traffic_metrics if available (else show UNKNOWN)
- LLM rationale field: if NULL, show "pending (added in semantic phase)"
- Approve/Reject/Defer buttons: status update AND audit_log in ONE transaction
- Comment required for all three actions

Impact analysis panel:
- Search by project_name (ILIKE match, show first result)
- Upstream: all api_edges where target_node_id = searched node
  — show caller project_name, layer, source_endpoint_path → target_endpoint_path
- Downstream: all api_edges where source_node_id = searched node
  — same format
- If upstream is empty: "None — this is an entry point"
- If downstream is empty: "None — this is a terminal node"
```

**Verify:**
- Merge candidate count matches `SELECT COUNT(*) FROM merge_candidates WHERE status='pending'`
- Approve one candidate → `status` = 'approved', `audit_log` row present with `entity_type='merge_candidate'`
- Impact analysis for a known Proc node → upstream shows its Exp caller, downstream shows its Sys callee
- Impact for a terminal Sys node → downstream shows "None"

---

## M12 — Refresh, Snapshots & Audit Trail

**Goal:** Scheduled weekly refresh that re-runs traversal and detection,
creates a `graph_snapshots` row, logs edge changes to `edge_history`, and
diffs findings into new/resolved/persisting.

**Agent prompt:**
```
Build scripts/refresh.py with a function run_refresh() that:

1. Creates one ingestion_runs row (status='running')
2. Re-ingests nodes and edges from source (or detects changes from last run)
3. Compares current api_edges to previous run:
   - Edges present now but absent before → edge_history row, event_type='appeared'
   - Edges absent now but present before → edge_history row, event_type='disappeared'
4. Re-runs materialize_flows() — new flows linked to this run's snapshot_id
5. Creates one graph_snapshots row with node_count, edge_count, run_id
6. Re-runs all four detection rules — new findings linked to snapshot_id
7. Diffs new findings against previous snapshot:
   - finding with same pattern_type and node_ids exists in previous snapshot
     and review_status != 'dismissed' → tag as 'persisting'
   - New finding not in previous → tag as 'new' in detail JSONB
   - Finding in previous but not in current → tag as 'resolved' in detail JSONB
8. Updates ingestion_runs row to status='completed'

Wire into APScheduler for weekly runs OR provide a cron entry.
Also expose run_refresh() as a callable from the Streamlit UI
(a "Run refresh now" button on the Findings Dashboard).
```

**Verify:**
```sql
-- After running refresh:
SELECT run_id, status, nodes_created, edges_created
FROM ingestion_runs ORDER BY started_at DESC LIMIT 1;

-- Snapshot linked to run
SELECT snapshot_id, node_count, edge_count
FROM graph_snapshots ORDER BY taken_at DESC LIMIT 1;

-- Flows and findings linked to this snapshot
SELECT COUNT(*) FROM flows
WHERE snapshot_id = (SELECT snapshot_id FROM graph_snapshots
                     ORDER BY taken_at DESC LIMIT 1);

SELECT COUNT(*) FROM structural_findings
WHERE snapshot_id = (SELECT snapshot_id FROM graph_snapshots
                     ORDER BY taken_at DESC LIMIT 1);

-- Edge history (if any edges changed)
SELECT event_type, COUNT(*)
FROM edge_history
WHERE detected_in_run = (SELECT run_id FROM ingestion_runs
                         ORDER BY started_at DESC LIMIT 1)
GROUP BY event_type;

-- Finding diff tags in detail JSONB
SELECT detail->>'diff_status', COUNT(*)
FROM structural_findings
WHERE snapshot_id = (SELECT snapshot_id FROM graph_snapshots
                     ORDER BY taken_at DESC LIMIT 1)
GROUP BY detail->>'diff_status';
```
