# Data Ingestion Guide
## Mule API Structural Detection Platform — Phase 1

**What this covers:** the source JSON format for Phase 1, the Python
ingestion pipeline, verification SQL, and the edge-diff logic for refresh.

**What is NOT in this guide:** field-level structured data (`api_fields`),
vector embeddings (`node_embeddings`), and raw spec storage (`api_specs`)
are all deferred to later phases. The source format here is deliberately
simpler — just what is needed to build and detect structural patterns in
the call graph.

---

## 1. Source data format

### 1.1 Per-API JSON document

This is the shape your Bitbucket LLM extraction must produce for each
Mule project. The `calls[]` array is how edges enter the system.

```json
{
  "project_name":      "proc-nach-debit-api",
  "layer":             "proc",
  "domain":            "payments",
  "functionality":     "NACH Debit Processing",
  "owning_team":       "payments-platform",
  "listener_endpoint": "/proc/v1/nach/debit/initiate",
  "purpose_text":      "Orchestrates NACH debit — validates mandate, checks limits, submits to clearance.",
  "repo_name":         "mule-proc-nach-debit",
  "repo_url":          "https://bitbucket.org/org/mule-proc-nach-debit",
  "status":            "active",
  "calls": [
    {
      "target_project":  "sys-nach-clearance-api",
      "source_endpoint": "/proc/v1/nach/debit/initiate",
      "target_endpoint": "/nach/v2/clearance/submit",
      "call_type":       "sync"
    }
  ]
}
```

**Field rules:**
- `layer` must be one of `exp`, `proc`, `sys` — reject otherwise
- `calls` may be an empty list `[]` for Sys-layer APIs (terminal nodes)
- `purpose_text` must be specific — not "This is a microservice"
  (poor purpose_text does not break Phase 1 but will hurt Phase 2 retrieval)
- `domain` must match a canonical name — normalised in M1b
- `project_name` must be globally unique across all Mule projects

### 1.2 Batch file format

A single JSON file containing a list of API documents:

```json
[
  { "project_name": "exp-nach-debit-api", "layer": "exp", ... },
  { "project_name": "proc-nach-debit-api", "layer": "proc", ... },
  { "project_name": "sys-nach-clearance-api", "layer": "sys", ... }
]
```

### 1.3 What is intentionally NOT required in Phase 1

| Field | Phase 1 | Why not required yet |
|---|---|---|
| `request_fields_structured` | Not required | api_fields table is Reserved |
| `response_fields_structured` | Not required | api_fields table is Reserved |
| `business_rules` | Not required | No composition validator yet |
| `error_codes` | Not required | Not used in structural detection |
| `sample_request` / `sample_response` | Not required | api_specs is Reserved |

Adding these fields to your source documents now does no harm — they will
just be ignored during ingestion and used in a later phase.

---

## 2. Ingestion pipeline (complete Python)

```python
# scripts/ingest.py
import json
import psycopg2
from psycopg2.extras import execute_values, RealDictCursor
from datetime import datetime

DB_URL = "postgresql://user:password@localhost:5432/api_governance"

def get_conn():
    return psycopg2.connect(DB_URL)


def start_run(run_type: str, conn) -> int:
    with conn.cursor() as cur:
        cur.execute(\"\"\"
            INSERT INTO ingestion_runs (run_type, status, started_at)
            VALUES (%s, 'running', NOW())
            RETURNING run_id
        \"\"\", (run_type,))
        run_id = cur.fetchone()[0]
    conn.commit()
    return run_id


def finish_run(run_id: int, stats: dict, conn):
    with conn.cursor() as cur:
        cur.execute(\"\"\"
            UPDATE ingestion_runs SET
                completed_at    = NOW(),
                repos_scanned   = %s,
                repos_succeeded = %s,
                repos_failed    = %s,
                nodes_created   = %s,
                edges_created   = %s,
                status          = 'completed'
            WHERE run_id = %s
        \"\"\", (stats['scanned'], stats['succeeded'], stats['failed'],
                stats['nodes'], stats['edges'], run_id))
    conn.commit()


def insert_node(doc: dict, conn) -> int | None:
    \"\"\"Insert one API node. Returns node_id or None if rejected.\"\"\"
    if doc['layer'] not in ('exp', 'proc', 'sys'):
        print(f"  REJECTED {doc['project_name']}: layer '{doc['layer']}' invalid")
        return None

    with conn.cursor() as cur:
        cur.execute(\"\"\"
            INSERT INTO api_nodes
                (project_name, layer, listener_endpoint, functionality,
                 domain, purpose_text, owning_team, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (project_name) DO UPDATE
                SET listener_endpoint = EXCLUDED.listener_endpoint,
                    functionality     = EXCLUDED.functionality,
                    domain            = EXCLUDED.domain,
                    purpose_text      = EXCLUDED.purpose_text,
                    owning_team       = EXCLUDED.owning_team,
                    status            = EXCLUDED.status
            RETURNING node_id
        \"\"\", (
            doc['project_name'],
            doc['layer'],
            doc.get('listener_endpoint'),
            doc.get('functionality'),
            doc.get('domain'),
            doc.get('purpose_text'),
            doc.get('owning_team'),
            doc.get('status', 'active')
        ))
        node_id = cur.fetchone()[0]
    conn.commit()
    return node_id


def insert_edges(doc: dict, node_map: dict[str, int], conn) -> int:
    \"\"\"Insert all outbound edges for one API. Returns count inserted.\"\"\"
    source_id = node_map.get(doc['project_name'])
    if not source_id:
        return 0

    inserted = 0
    for call in doc.get('calls', []):
        target_id = node_map.get(call['target_project'])
        if not target_id:
            print(f"  SKIP edge {doc['project_name']} → {call['target_project']}: "
                  f"target not found")
            continue
        try:
            with conn.cursor() as cur:
                cur.execute(\"\"\"
                    INSERT INTO api_edges
                        (source_node_id, target_node_id,
                         source_project_name, target_project_name,
                         source_endpoint_path, target_endpoint_path,
                         call_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                \"\"\", (
                    source_id, target_id,
                    doc['project_name'], call['target_project'],
                    call.get('source_endpoint'),
                    call.get('target_endpoint'),
                    call.get('call_type', 'sync')
                ))
            conn.commit()
            inserted += 1
        except Exception as e:
            print(f"  ERROR edge: {e}")
            conn.rollback()

    return inserted


def insert_source_repo(doc: dict, node_id: int, run_id: int, conn):
    with conn.cursor() as cur:
        cur.execute(\"\"\"
            INSERT INTO source_repos
                (repo_name, repo_url, last_scanned_at, extraction_status, node_id)
            VALUES (%s, %s, NOW(), 'success', %s)
            ON CONFLICT (repo_name) DO UPDATE
                SET last_scanned_at   = NOW(),
                    extraction_status = 'success',
                    node_id           = EXCLUDED.node_id
        \"\"\", (doc.get('repo_name', doc['project_name']),
                doc.get('repo_url'), node_id))
    conn.commit()


def load_from_file(json_path: str):
    \"\"\"Full ingestion pipeline. Call this to load a batch of API docs.\"\"\"
    conn  = get_conn()
    stats = {'scanned': 0, 'succeeded': 0, 'failed': 0, 'nodes': 0, 'edges': 0}

    with open(json_path) as f:
        docs = json.load(f)

    run_id = start_run('full_scan', conn)
    print(f"Ingestion run #{run_id} started — {len(docs)} APIs")

    # Pass 1: insert all nodes first (so edges can resolve names)
    node_map: dict[str, int] = {}
    for doc in docs:
        stats['scanned'] += 1
        node_id = insert_node(doc, conn)
        if node_id:
            node_map[doc['project_name']] = node_id
            stats['succeeded'] += 1
            stats['nodes'] += 1
        else:
            stats['failed'] += 1

    # Pass 2: insert all edges (all nodes now exist)
    for doc in docs:
        edge_count = insert_edges(doc, node_map, conn)
        stats['edges'] += edge_count

    # Pass 3: source repos
    for doc in docs:
        node_id = node_map.get(doc['project_name'])
        if node_id:
            insert_source_repo(doc, node_id, run_id, conn)

    finish_run(run_id, stats, conn)
    conn.close()

    print(f"\nRun #{run_id} complete:")
    print(f"  Nodes  : {stats['nodes']} created, {stats['failed']} rejected")
    print(f"  Edges  : {stats['edges']} inserted")
    return stats


if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else 'data/sample_apis.json'
    load_from_file(path)
```

---

## 3. Verification SQL

Run these immediately after ingestion to confirm everything landed correctly:

```sql
-- Core counts
SELECT
    (SELECT COUNT(*) FROM api_nodes WHERE status = 'active')  AS active_nodes,
    (SELECT COUNT(*) FROM api_edges)                           AS edges,
    (SELECT COUNT(*) FROM api_nodes WHERE layer = 'exp')       AS exp_nodes,
    (SELECT COUNT(*) FROM api_nodes WHERE layer = 'proc')      AS proc_nodes,
    (SELECT COUNT(*) FROM api_nodes WHERE layer = 'sys')       AS sys_nodes;

-- Ingestion run summary
SELECT run_id, status, repos_scanned, repos_succeeded, repos_failed,
       nodes_created, edges_created, started_at, completed_at
FROM ingestion_runs ORDER BY started_at DESC LIMIT 1;

-- Edges referencing unknown nodes (should be 0)
SELECT COUNT(*) FROM api_edges e
WHERE NOT EXISTS (SELECT 1 FROM api_nodes WHERE node_id = e.source_node_id)
   OR NOT EXISTS (SELECT 1 FROM api_nodes WHERE node_id = e.target_node_id);

-- Nodes with no outbound edges (Sys nodes and isolated nodes)
SELECT project_name, layer FROM api_nodes n
WHERE status = 'active'
  AND NOT EXISTS (SELECT 1 FROM api_edges WHERE source_node_id = n.node_id)
ORDER BY layer, project_name;
-- Expected: all sys-layer nodes, plus any exp/proc with no configured calls

-- Nodes with no inbound edges (Exp entry points)
SELECT project_name, layer FROM api_nodes n
WHERE status = 'active'
  AND NOT EXISTS (SELECT 1 FROM api_edges WHERE target_node_id = n.node_id)
ORDER BY layer, project_name;
-- Expected: all exp-layer nodes (no one calls them externally)

-- Source repo coverage
SELECT
    (SELECT COUNT(*) FROM source_repos WHERE extraction_status = 'success') AS ok,
    (SELECT COUNT(*) FROM source_repos WHERE extraction_status = 'failed')  AS failed,
    (SELECT COUNT(*) FROM api_nodes WHERE status = 'active')                AS nodes;
-- ok should equal nodes
```

---

## 4. Gate before running M2

**Three queries must all return zero before running M2 (Traversal & Rules):**

```sql
-- Gate 1: no active nodes without a domain value
SELECT COUNT(*) FROM api_nodes WHERE domain IS NULL AND status = 'active';

-- Gate 2: no active nodes without a domain_id (M1b must run first)
SELECT COUNT(*) FROM api_nodes WHERE domain_id IS NULL AND status = 'active';

-- Gate 3: no dangling edges
SELECT COUNT(*) FROM api_edges e
WHERE NOT EXISTS (SELECT 1 FROM api_nodes WHERE node_id = e.source_node_id AND status = 'active')
   OR NOT EXISTS (SELECT 1 FROM api_nodes WHERE node_id = e.target_node_id AND status = 'active');
```

All three must return `0`. If any return > 0, fix the ingestion data before running M2 — the traversal CTE will produce incorrect flows if nodes or domain mappings are missing.

---

## 5. Edge diff logic for refresh (M12)

The refresh job (M12) needs to compare the current set of edges against
the previous run to detect appeared/disappeared edges and write `edge_history`.

```python
# scripts/refresh.py — edge diff section

def get_edge_set(run_id: int, conn) -> set[tuple]:
    \"\"\"Get the set of (source_node_id, target_node_id) edges active at
    the time of a given ingestion run. Uses edge_history to reconstruct.\"\"\"
    # If first run, return empty set
    if run_id is None:
        return set()
    with conn.cursor() as cur:
        cur.execute(\"\"\"
            SELECT DISTINCT source_node_id, target_node_id
            FROM api_edges
        \"\"\")
        return {(r[0], r[1]) for r in cur.fetchall()}


def compute_edge_diff(prev_edges: set, curr_edges: set,
                      run_id: int, conn):
    \"\"\"Write edge_history rows for appeared and disappeared edges.\"\"\"
    appeared    = curr_edges - prev_edges
    disappeared = prev_edges - curr_edges

    rows = []
    for src, tgt in appeared:
        rows.append((src, tgt, 'appeared', run_id))
    for src, tgt in disappeared:
        rows.append((src, tgt, 'disappeared', run_id))

    if rows:
        with conn.cursor() as cur:
            execute_values(cur, \"\"\"
                INSERT INTO edge_history
                    (source_node_id, target_node_id, event_type, detected_in_run)
                VALUES %s
            \"\"\", rows)
        conn.commit()
        print(f"  Edge history: {len(appeared)} appeared, {len(disappeared)} disappeared")
    else:
        print("  Edge history: no changes detected")
```

---

## 6. Common issues and fixes

| Symptom | Cause | Fix |
|---|---|---|
| `api_edges` row count is 0 | `calls[]` array is empty in all source docs | Check extraction prompt — it must populate `calls` from HTTP client config in each Mule project |
| Edges skipped with "target not found" | Target project name in `calls[].target_project` does not match any `api_nodes.project_name` exactly | Confirm project_name is consistent in extraction — even a trailing space will cause a miss |
| All nodes have `domain = NULL` | Extraction prompt is not populating the domain field | Add domain to the extraction prompt |
| M2 produces 0 flows | No Exp nodes exist | Check layer assignment — all entry-point APIs must be `layer='exp'` |
| DUPLICATE_FLOW finding raises false positive for -v1/-v2 pair | M1b did not run, or api_versions not populated | Run M1b verify check — `SELECT COUNT(*) FROM api_versions` must be > 0 |
| `DEEP_CHAIN_THRESHOLD = 4` produces too many findings | Normal architecture uses 4-hop chains | Raise threshold to 5 in `core/rules.py` |
