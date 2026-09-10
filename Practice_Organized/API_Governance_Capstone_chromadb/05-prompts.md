# Agent Prompts
## Mule API Structural Detection Platform — Phase 1

Copy each prompt exactly as written. Paste into your coding agent at the
start of each milestone. Include the referenced sections from the SRS and
ingestion guide as attachments or pasted context — the agent needs the
full DDL and rule logic, not a summary of it.

---

## M1 — Schema & Data Load

```
You are building a Mule API governance platform. This milestone creates
the full database schema and loads sample data.

TASK:
1. Create all 19 PostgreSQL tables from the DDL I will paste below.
   Include CREATE EXTENSION IF NOT EXISTS vector even though node_embeddings
   will not be populated yet — it must exist now to avoid migration later.

2. Write a Python script scripts/ingest.py with a function
   load_sample_data(json_path: str, conn) that:
   - Reads a JSON file containing a list of API documents
   - Each document has the shape in 06-data-ingestion-guide.md Section 2
   - Inserts into api_nodes (reject if layer not in exp/proc/sys)
   - Inserts into api_edges by resolving project_name to node_id
     (reject edges where either project_name is not found in api_nodes)
   - Populates source_repos (one row per API)
   - Creates one ingestion_runs row and updates it on completion
   - Prints per-table row counts at the end

3. Do not populate: api_fields, node_embeddings, field_mappings,
   composition_candidates, llm_call_log, api_specs — these stay empty.

[PASTE: 01-srs.md Sections 2.1 through 2.21 DDL here]
[PASTE: 06-data-ingestion-guide.md Section 2 source format here]
```

---

## M1b — Taxonomy Seeding & Version Detection

```
You are building a Mule API governance platform. Schema and data are
already loaded (M1 complete). This milestone normalises domain vocabulary
and detects API version relationships.

TASK:
1. Read all distinct domain values from api_nodes.domain
2. Deduplicate: collapse case variants and obvious singular/plural
   differences into one canonical form. For any pair where you are
   unsure, print them and STOP — do not guess, ask me to confirm.
3. Insert canonical entries into domain_taxonomy
4. UPDATE api_nodes SET domain_id = <matching domain_taxonomy.domain_id>
   for every row. After updating, run:
   SELECT COUNT(*) FROM api_nodes WHERE domain_id IS NULL AND status='active'
   This MUST return 0 before proceeding.

5. Scan api_nodes.project_name for version suffixes:
   - Patterns to detect: -v1, -v2, -v3, -v4, -YYYY-MM date suffixes
   - For each detected pair (e.g. proc-payment-api-v1 and proc-payment-api-v2):
     Insert into api_versions linking both to the same lineage
     Mark the higher version as is_current=TRUE, lower as FALSE
   - If you detect a suffix but cannot find a matching counterpart
     (e.g. -v2 exists but no -v1), print it and flag for manual review
     rather than guessing.

Print: domains seeded, nodes updated with domain_id, version pairs detected.
```

---

## M2 — Traversal & Structural Detection

```
You are building a Mule API governance platform. Schema is created, data
is loaded, taxonomy is seeded (M1 and M1b complete).

TASK:
1. Implement materialize_flows(conn) using the recursive CTE in
   01-srs.md Section 4. Truncate flows before inserting (this function
   rebuilds from scratch on each call). Print the row count inserted.

2. Build a networkx DiGraph from api_nodes and api_edges:
   - Nodes: all api_nodes where status='active'
   - Edges: all api_edges
   - Node attributes: layer, domain, project_name, domain_id

3. Implement these four functions from 01-srs.md Section 5 EXACTLY as
   specified — do not change the logic:
   - find_duplicate_flows(flows_df, conn)
     IMPORTANT: before raising any finding, call same_version_lineage(a, b, conn)
     which queries api_versions to check if nodes a and b are different versions
     of the same API. If they are, skip this pair entirely.
   - find_pass_through_hops(G, id_to_name)
   - find_deep_chains(flows_df, id_to_name)
   - find_fan_in_clusters(G, id_to_name)

4. For each DUPLICATE_FLOW finding, also INSERT a merge_candidates row:
   - node_a_id = min(root_exp_id_a, root_exp_id_b) of the pair
   - node_b_id = max(root_exp_id_a, root_exp_id_b)
   - structural_score = result of structural_score() from Section 5.5
   - semantic_score = NULL (added later)
   - llm_rationale = NULL (added later)
   - status = 'pending'

5. Write all findings to structural_findings. Print count per pattern_type.

[PASTE: 01-srs.md Section 4 recursive CTE here]
[PASTE: 01-srs.md Section 5 rule logic here]
```

---

## M7 — Core Module Assembly

```
You are building a Mule API governance platform. All logic is working
(M1, M1b, M2 verified). This milestone reorganises code into the core/
package — NO LOGIC CHANGES, only code movement and type hints.

TASK:
Create these files with these exact public function signatures:

core/db.py
  get_conn() -> psycopg2.connection

core/graph.py
  build_graph(conn) -> nx.DiGraph
  get_node_names(conn) -> dict[int, str]   # node_id -> project_name

core/traversal.py
  materialize_flows(conn) -> int           # returns row count inserted
  get_flows_df(conn) -> pd.DataFrame       # reads flows table into DataFrame

core/rules.py
  find_duplicate_flows(flows_df: pd.DataFrame, conn) -> list[dict]
  find_pass_through_hops(G: nx.DiGraph, id_to_name: dict) -> list[dict]
  find_deep_chains(flows_df: pd.DataFrame, id_to_name: dict) -> list[dict]
  find_fan_in_clusters(G: nx.DiGraph, id_to_name: dict) -> list[dict]
  run_all_rules(conn) -> list[dict]        # calls all four, returns combined list
  write_findings(findings: list[dict], conn) -> int  # inserts, returns count
  structural_score(flow_a_len: int, flow_b_len: int, same_domain: bool) -> float

Move code from scripts/ into these modules. Do not change any logic.
Add a docstring to each public function. Add type hints to all signatures.
Confirm by importing and running a quick integration test:

  from core.rules import run_all_rules
  findings = run_all_rules(get_conn())
  print(len(findings))  # must match M2 finding count exactly
```

---

## M8 — Streamlit: Graph Explorer & Findings Dashboard

```
You are building a Mule API governance platform. core/ package is complete
(M7 verified). Build two Streamlit screens.

TASK:
Build app/1_Graph_Explorer.py and app/2_Findings_Dashboard.py exactly as
specified in 03-ui-design.md Sections 1 and 2. Do not add features not in
the spec — implement exactly what is described.

Critical requirements to implement correctly:

1. Layer colours (exact hex): exp=#4C72B0, proc=#DD8452, sys=#55A868
2. Node size: 15 + min(G.in_degree(nid) * 5, 35)
3. Finding overlay: when "Show findings" is checked, nodes in open
   structural_findings get colour #E74C3C instead of their layer colour
4. Approve and Dismiss in Findings Dashboard: BOTH the UPDATE
   structural_findings and the INSERT audit_log must be inside a single
   WITH conn: WITH conn.cursor() as cur: block. If they are in separate
   commits, this is wrong.
5. Comment is required for both Approve and Dismiss. If comment is empty,
   show st.warning() and do NOT write to the database.
6. "View in graph" button: set st.session_state['filter_node'] = node_id
   then call st.switch_page("pages/1_Graph_Explorer.py")
7. Use streamlit-agraph for graph rendering
8. Import from core/ — no raw SQL in the Streamlit pages except for the
   finding status update transaction (which needs the conn context directly)

[PASTE: 03-ui-design.md Section 1 full layout and behaviour code]
[PASTE: 03-ui-design.md Section 2 full layout and behaviour code]
```

---

## M10 — Streamlit: Merge Candidates & Impact Analysis

```
You are building a Mule API governance platform. Graph Explorer and
Findings Dashboard are live (M8 verified). Build the third screen.

TASK:
Build app/3_Merge_Impact.py exactly as specified in 03-ui-design.md
Section 3. Two panels side by side (st.columns([1,1])).

Merge candidates panel requirements:
1. Query merge_candidates WHERE status='pending', ORDER BY structural_score DESC
2. Join to api_nodes to get project_name for node_a and node_b
3. Join to domain_taxonomy to show same/different domain
4. Join to traffic_metrics (latest date, aggregate daily_hits) for traffic risk.
   If no traffic_metrics rows exist for this node, show traffic_risk='UNKNOWN'
5. If llm_rationale IS NULL, show the grey italic text:
   "pending — added in semantic detection phase"
6. Approve/Reject/Defer: ALL THREE must do UPDATE merge_candidates + INSERT
   audit_log in a single transaction. Comment required for all three.
7. After any action, call st.rerun() to refresh the candidate list.

Impact analysis panel requirements:
1. Text input — search by project_name using ILIKE '%search%'
2. Show upstream: api_edges WHERE target_node_id = found node
   Display: caller project_name, layer badge, source and target endpoint paths
3. Show downstream: api_edges WHERE source_node_id = found node
   Same display format
4. Empty upstream: st.caption("None — this is an entry point")
5. Empty downstream: st.caption("None — this is a terminal node")

[PASTE: 03-ui-design.md Section 3 full layout and behaviour code]
```

---

## M12 — Refresh, Snapshots & Audit Trail

```
You are building a Mule API governance platform. All three screens are live
(M8 and M10 verified). Build the weekly refresh job.

TASK:
Build scripts/refresh.py with a run_refresh(conn) function that runs the
following steps in order. Each step must complete before the next starts.

Step 1: Create ingestion_runs row with status='running'
Step 2: Load any changed nodes/edges (or re-load everything if simpler)
Step 3: Edge diff vs previous run
  - Get all edges from the PREVIOUS completed run's snapshot
  - Compare to current api_edges
  - Insert edge_history rows:
    event_type='appeared'     for edges in current but not previous
    event_type='disappeared'  for edges in previous but not current
    detected_in_run = this run's run_id
Step 4: materialize_flows(conn) — rebuilds flows table
Step 5: Create graph_snapshots row with node_count, edge_count, run_id
  - UPDATE flows SET snapshot_id = new snapshot_id
Step 6: run_all_rules(conn) — re-runs all four detectors
Step 7: Finding diff — for each new finding:
  - If same pattern_type AND same node_ids[] exists in previous snapshot
    findings: set detail['diff_status'] = 'persisting'
  - Else: set detail['diff_status'] = 'new'
  - For findings in previous snapshot not in current: UPDATE that finding's
    detail to add diff_status='resolved'
  Write findings with snapshot_id = new snapshot_id
Step 8: Update ingestion_runs SET status='completed', completed_at=NOW()

Expose run_refresh as both:
- A standalone script: if __name__ == '__main__': run_refresh(get_conn())
- A function importable from Streamlit for the "Run refresh now" button

Wire APScheduler to call run_refresh every Monday at 02:00 local time,
OR provide a crontab entry as a comment at the top of the file.
```
