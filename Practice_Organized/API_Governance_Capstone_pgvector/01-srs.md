# Software Requirements Specification
## Mule API Structural Detection Platform — Phase 1

**Scope:** Detect structural redundancy in the Mule API call graph and surface
findings through a Streamlit UI with an architect review workflow.

**Deliberately excluded from this phase:**
- Vector embeddings and semantic similarity (no pgvector populated yet)
- LLM integration (no calls to internal LLM)
- Composition advisory and field mapping
- API Discovery semantic search

The full 19-table schema is created in M1 so no migration is needed when
semantic and composition features are added. Only the tables marked
**Populated** below are written to in this phase.

---

## 1. System overview

```
Bitbucket repos (Mule projects)
        │
        ▼
LLM extraction → per-API JSON (project_name, layer, domain,
                               purpose_text, calls[], owning_team)
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  INGESTION (M1)                                     │
│  api_nodes  +  api_edges  +  domain_taxonomy        │
│  api_versions  +  source_repos  +  ingestion_runs   │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  STRUCTURAL DETECTION (M2)                          │
│  Recursive CTE → flows                              │
│  4 rules → structural_findings                      │
│  Structural score → merge_candidates (no LLM yet)   │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  STREAMLIT UI                                       │
│  Graph Explorer  (M8)                               │
│  Findings Dashboard  (M8)                           │
│  Merge Candidates + Impact Analysis  (M10)          │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  REFRESH (M12)                                      │
│  graph_snapshots  +  edge_history  +  finding diff  │
└─────────────────────────────────────────────────────┘
```

---

## 2. Complete schema (19 tables)

Tables marked **Populated** are written to in this phase.
Tables marked **Reserved** are created now, written to in a later phase.
All DDL runs in M1 so no migration is ever needed.

### 2.1 `domain_taxonomy` — **Populated**

```sql
CREATE TABLE domain_taxonomy (
    domain_id    SERIAL PRIMARY KEY,
    domain_name  VARCHAR(100) NOT NULL UNIQUE,
    description  TEXT,
    parent_domain_id INT REFERENCES domain_taxonomy(domain_id)
);
```

Seed with canonical domain names before ingesting nodes.
`api_nodes.domain_id` is a foreign key into this table — prevents free-text
variants ("payments" vs "Payments") from fragmenting fan-in clustering.

### 2.2 `functionality_taxonomy` — **Reserved**

```sql
CREATE TABLE functionality_taxonomy (
    functionality_id   SERIAL PRIMARY KEY,
    functionality_name VARCHAR(255) NOT NULL UNIQUE,
    domain_id          INT REFERENCES domain_taxonomy(domain_id),
    description        TEXT
);
```

### 2.3 `team_directory` — **Populated**

```sql
CREATE TABLE team_directory (
    team_id         SERIAL PRIMARY KEY,
    team_name       VARCHAR(100) NOT NULL UNIQUE,
    department      VARCHAR(100),
    contact_channel VARCHAR(255)
);
```

### 2.4 `api_nodes` — **Populated**

```sql
CREATE TABLE api_nodes (
    node_id           SERIAL PRIMARY KEY,
    project_name      VARCHAR(255) NOT NULL UNIQUE,
    layer             VARCHAR(10)  NOT NULL CHECK (layer IN ('exp','proc','sys')),
    listener_endpoint VARCHAR(500),
    functionality     VARCHAR(255),
    domain            VARCHAR(100),
    domain_id         INT REFERENCES domain_taxonomy(domain_id),
    functionality_id  INT REFERENCES functionality_taxonomy(functionality_id),
    team_id           INT REFERENCES team_directory(team_id),
    purpose_text      TEXT,
    owning_team       VARCHAR(100),
    status            VARCHAR(20) DEFAULT 'active',
    merged_into       INT REFERENCES api_nodes(node_id),
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_nodes_layer    ON api_nodes(layer);
CREATE INDEX idx_nodes_domain   ON api_nodes(domain_id);
CREATE INDEX idx_nodes_status   ON api_nodes(status);
```

### 2.5 `api_edges` — **Populated**

```sql
CREATE TABLE api_edges (
    edge_id               SERIAL PRIMARY KEY,
    source_node_id        INT NOT NULL REFERENCES api_nodes(node_id),
    target_node_id        INT NOT NULL REFERENCES api_nodes(node_id),
    source_project_name   VARCHAR(255),
    target_project_name   VARCHAR(255),
    source_endpoint_path  VARCHAR(500),
    target_endpoint_path  VARCHAR(500),
    call_type             VARCHAR(20) DEFAULT 'sync',
    discovered_at         TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(source_node_id, target_node_id,
           source_endpoint_path, target_endpoint_path)
);

CREATE INDEX idx_edges_source ON api_edges(source_node_id);
CREATE INDEX idx_edges_target ON api_edges(target_node_id);
```

### 2.6 `api_fields` — **Reserved**

```sql
CREATE TABLE api_fields (
    field_id     SERIAL PRIMARY KEY,
    node_id      INT NOT NULL REFERENCES api_nodes(node_id),
    direction    VARCHAR(10) NOT NULL CHECK (direction IN ('request','response')),
    field_path   VARCHAR(255) NOT NULL,
    field_name   VARCHAR(100) NOT NULL,
    data_type    VARCHAR(30),
    is_required  BOOLEAN DEFAULT FALSE,
    description  TEXT,
    sample_value TEXT
);
```

### 2.7 `source_repos` — **Populated**

```sql
CREATE TABLE source_repos (
    repo_id           SERIAL PRIMARY KEY,
    repo_name         VARCHAR(255) NOT NULL UNIQUE,
    repo_url          VARCHAR(500),
    last_scanned_at   TIMESTAMPTZ,
    last_commit_sha   VARCHAR(64),
    extraction_status VARCHAR(20) DEFAULT 'pending',
    extraction_error  TEXT,
    node_id           INT REFERENCES api_nodes(node_id),
    created_at        TIMESTAMPTZ DEFAULT NOW()
);
```

### 2.8 `ingestion_runs` — **Populated**

```sql
CREATE TABLE ingestion_runs (
    run_id          SERIAL PRIMARY KEY,
    run_type        VARCHAR(30) NOT NULL,
    started_at      TIMESTAMPTZ DEFAULT NOW(),
    completed_at    TIMESTAMPTZ,
    repos_scanned   INT DEFAULT 0,
    repos_succeeded INT DEFAULT 0,
    repos_failed    INT DEFAULT 0,
    nodes_created   INT DEFAULT 0,
    nodes_updated   INT DEFAULT 0,
    edges_created   INT DEFAULT 0,
    status          VARCHAR(20) DEFAULT 'running',
    error_summary   TEXT
);
```

### 2.9 `api_versions` — **Populated**

```sql
CREATE TABLE api_versions (
    version_id    SERIAL PRIMARY KEY,
    node_id       INT NOT NULL REFERENCES api_nodes(node_id),
    version_label VARCHAR(20) NOT NULL,
    is_current    BOOLEAN DEFAULT TRUE,
    superseded_by INT REFERENCES api_versions(version_id),
    released_at   TIMESTAMPTZ,
    deprecated_at TIMESTAMPTZ,
    UNIQUE(node_id, version_label)
);
```

> Critical for correctness: the duplicate-flow rule checks `api_versions`
> before flagging a finding. If two nodes are different versions of the same
> API lineage, the finding is suppressed — they are not redundant, just versioned.

### 2.10 `api_specs` — **Reserved**

```sql
CREATE TABLE api_specs (
    spec_id           SERIAL PRIMARY KEY,
    node_id           INT NOT NULL REFERENCES api_nodes(node_id),
    spec_format       VARCHAR(20),
    raw_content       TEXT,
    source_repo_id    INT REFERENCES source_repos(repo_id),
    extraction_run_id INT REFERENCES ingestion_runs(run_id),
    ingested_at       TIMESTAMPTZ DEFAULT NOW()
);
```

### 2.11 `flows` — **Populated**

```sql
CREATE TABLE flows (
    flow_id         SERIAL PRIMARY KEY,
    root_exp_id     INT NOT NULL REFERENCES api_nodes(node_id),
    node_path       INT[]  NOT NULL,
    endpoint_path   TEXT[],
    hop_count       INT NOT NULL,
    terminal_sys_id INT REFERENCES api_nodes(node_id),
    snapshot_id     INT,
    built_at        TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_flows_root     ON flows(root_exp_id);
CREATE INDEX idx_flows_terminal ON flows(terminal_sys_id);
CREATE INDEX idx_flows_snapshot ON flows(snapshot_id);
```

### 2.12 `structural_findings` — **Populated**

```sql
CREATE TABLE structural_findings (
    finding_id    SERIAL PRIMARY KEY,
    pattern_type  VARCHAR(40) NOT NULL,
    node_ids      INT[]  NOT NULL,
    severity      VARCHAR(10),
    detail        JSONB,
    snapshot_id   INT,
    detected_at   TIMESTAMPTZ DEFAULT NOW(),
    review_status VARCHAR(20) DEFAULT 'open'
);

CREATE INDEX idx_findings_pattern  ON structural_findings(pattern_type);
CREATE INDEX idx_findings_status   ON structural_findings(review_status);
CREATE INDEX idx_findings_snapshot ON structural_findings(snapshot_id);
```

`detail` JSONB shape per pattern type:

```json
// DUPLICATE_FLOW
{
  "terminal_node": "sys-crm-api",
  "flow_a": ["exp-customer-360-api", "proc-customer-orchestration-api", "sys-crm-api"],
  "flow_b": ["exp-account-summary-api", "proc-account-lookup-api", "sys-crm-api"]
}

// PASS_THROUGH_HOP
{
  "proc_node": "proc-order-status-api",
  "only_calls": "sys-oms-api",
  "called_by": ["exp-order-status-api"]
}

// DEEP_CHAIN
{
  "hop_count": 4,
  "path": ["exp-claims-intake-api", "proc-claims-validate-api",
           "proc-claims-route-api", "sys-policy-api"]
}

// FAN_IN_CLUSTER
{
  "sys_node": "sys-crm-api",
  "in_degree": 3,
  "callers": ["proc-customer-orchestration-api",
              "proc-account-lookup-api",
              "proc-notification-prefs-api"]
}
```

### 2.13 `merge_candidates` — **Populated** (structural score only, no LLM)

```sql
CREATE TABLE merge_candidates (
    candidate_id     SERIAL PRIMARY KEY,
    node_a_id        INT NOT NULL REFERENCES api_nodes(node_id),
    node_b_id        INT NOT NULL REFERENCES api_nodes(node_id),
    structural_score DECIMAL(5,4),
    semantic_score   DECIMAL(5,4),   -- NULL in this phase
    traffic_risk     VARCHAR(10),
    recommendation   VARCHAR(20),
    confidence       VARCHAR(10),
    llm_rationale    TEXT,            -- NULL in this phase
    status           VARCHAR(20) DEFAULT 'pending',
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    CHECK (node_a_id < node_b_id)
);
```

In this phase, `merge_candidates` is populated only for DUPLICATE_FLOW
findings where both chains reach the same terminal. `structural_score` is
set from graph-shape evidence alone. `semantic_score` and `llm_rationale`
remain NULL until the semantic detection phase.

### 2.14 `composition_candidates` — **Reserved**

```sql
CREATE TABLE composition_candidates (
    composition_id             SERIAL PRIMARY KEY,
    requirement_text           TEXT NOT NULL,
    node_sequence              INT[] NOT NULL,
    similarity_score           DECIMAL(5,4),
    schema_compatibility_score DECIMAL(5,4),
    domain_alignment_score     DECIMAL(5,4),
    composition_confidence     DECIMAL(5,4),
    recommendation             VARCHAR(20),
    llm_rationale              TEXT,
    status                     VARCHAR(20) DEFAULT 'proposed',
    created_at                 TIMESTAMPTZ DEFAULT NOW()
);
```

### 2.15 `field_mappings` — **Reserved**

```sql
CREATE TABLE field_mappings (
    mapping_id           SERIAL PRIMARY KEY,
    source_node_id       INT NOT NULL REFERENCES api_nodes(node_id),
    target_node_id       INT NOT NULL REFERENCES api_nodes(node_id),
    source_field_id      INT NOT NULL REFERENCES api_fields(field_id),
    target_field_id      INT NOT NULL REFERENCES api_fields(field_id),
    match_type           VARCHAR(20),
    confidence           DECIMAL(5,4),
    type_compatible      BOOLEAN,
    UNIQUE(source_node_id, target_node_id, source_field_id, target_field_id)
);
```

### 2.16 `traffic_metrics` — **Populated** (if available)

```sql
CREATE TABLE traffic_metrics (
    metric_id      SERIAL PRIMARY KEY,
    node_id        INT NOT NULL REFERENCES api_nodes(node_id),
    measured_date  DATE NOT NULL,
    daily_hits     BIGINT DEFAULT 0,
    p95_latency_ms DECIMAL(8,2),
    p99_latency_ms DECIMAL(8,2),
    UNIQUE(node_id, measured_date)
);
```

Used in the Findings Dashboard to show traffic risk on a Sys node before
recommending a merge. Load from Anypoint monitoring exports if available;
leave empty if not — platform works without it.

### 2.17 `audit_log` — **Populated**

```sql
CREATE TABLE audit_log (
    log_id      SERIAL PRIMARY KEY,
    entity_type VARCHAR(30),
    entity_id   INT NOT NULL,
    action      VARCHAR(30),
    comment     TEXT,
    reviewer    VARCHAR(100),
    acted_at    TIMESTAMPTZ DEFAULT NOW()
);
```

### 2.18 `llm_call_log` — **Reserved**

```sql
CREATE TABLE llm_call_log (
    call_id       SERIAL PRIMARY KEY,
    call_type     VARCHAR(40) NOT NULL,
    entity_id     INT,
    system_prompt TEXT,
    user_prompt   TEXT,
    llm_response  TEXT,
    tokens_used   INT,
    latency_ms    INT,
    called_at     TIMESTAMPTZ DEFAULT NOW()
);
```

### 2.19 `graph_snapshots` — **Populated**

```sql
CREATE TABLE graph_snapshots (
    snapshot_id SERIAL PRIMARY KEY,
    run_id      INT REFERENCES ingestion_runs(run_id),
    node_count  INT,
    edge_count  INT,
    taken_at    TIMESTAMPTZ DEFAULT NOW()
);
```

### 2.20 `edge_history` — **Populated**

```sql
CREATE TABLE edge_history (
    history_id           SERIAL PRIMARY KEY,
    source_node_id       INT NOT NULL REFERENCES api_nodes(node_id),
    target_node_id       INT NOT NULL REFERENCES api_nodes(node_id),
    source_endpoint_path VARCHAR(500),
    target_endpoint_path VARCHAR(500),
    event_type           VARCHAR(20) NOT NULL,
    detected_in_run      INT REFERENCES ingestion_runs(run_id),
    event_at             TIMESTAMPTZ DEFAULT NOW()
);
```

### 2.21 `node_embeddings` — **Reserved**

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE node_embeddings (
    embedding_id SERIAL PRIMARY KEY,
    node_id      INT NOT NULL REFERENCES api_nodes(node_id),
    chunk_type   VARCHAR(30) NOT NULL,
    embed_text   TEXT NOT NULL,
    embedding    VECTOR(1536),
    updated_at   TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(node_id, chunk_type)
);
```

---

## 3. Table inventory

| Table | Phase 1 status | Written in |
|---|---|---|
| `domain_taxonomy` | Populated | M1 |
| `functionality_taxonomy` | Reserved | Later |
| `team_directory` | Populated | M1 |
| `api_nodes` | Populated | M1 |
| `api_edges` | Populated | M1 |
| `api_fields` | Reserved | Later |
| `source_repos` | Populated | M1 |
| `ingestion_runs` | Populated | M1 |
| `api_versions` | Populated | M1b |
| `api_specs` | Reserved | Later |
| `flows` | Populated | M2 |
| `structural_findings` | Populated | M2 |
| `merge_candidates` | Populated (structural only) | M2 |
| `composition_candidates` | Reserved | Later |
| `field_mappings` | Reserved | Later |
| `traffic_metrics` | Populated if available | M1 |
| `audit_log` | Populated | M8/M10 |
| `llm_call_log` | Reserved | Later |
| `graph_snapshots` | Populated | M12 |
| `edge_history` | Populated | M12 |
| `node_embeddings` | Reserved | Later |

---

## 4. Traversal — recursive CTE

Materialises all paths from every Exp node to every reachable terminal,
up to MAX_HOPS depth. Result is written to `flows`.

```sql
WITH RECURSIVE traverse AS (
    -- Base: every active Exp node starts a path
    SELECT
        n.node_id           AS root_exp_id,
        n.node_id           AS current_node,
        ARRAY[n.node_id]    AS node_path,
        ARRAY[n.listener_endpoint::TEXT] AS endpoint_path,
        1                   AS hop_count,
        n.layer             AS current_layer
    FROM api_nodes n
    WHERE n.layer  = 'exp'
      AND n.status = 'active'

    UNION ALL

    -- Recurse: follow each outbound edge
    SELECT
        t.root_exp_id,
        e.target_node_id,
        t.node_path    || e.target_node_id,
        t.endpoint_path || e.target_endpoint_path::TEXT,
        t.hop_count + 1,
        n.layer
    FROM traverse t
    JOIN api_edges e ON e.source_node_id = t.current_node
    JOIN api_nodes n ON n.node_id = e.target_node_id
    WHERE t.hop_count < 6              -- max depth guard
      AND NOT (e.target_node_id = ANY(t.node_path))  -- cycle guard
      AND n.status = 'active'
)
SELECT
    root_exp_id,
    node_path,
    endpoint_path,
    hop_count,
    CASE WHEN current_layer = 'sys' THEN current_node END AS terminal_sys_id
FROM traverse
WHERE hop_count >= 2;   -- minimum meaningful path is at least 2 hops
```

---

## 5. Structural detection rules

### 5.1 DUPLICATE_FLOW

Two or more distinct Exp APIs each have a flow that terminates at the same
Sys API. One chain is a candidate for retirement.

**Version check (mandatory):** before raising this finding, confirm the two
root Exp nodes are not different versions of the same API lineage via
`api_versions`. If they are, suppress the finding.

```python
def find_duplicate_flows(flows_df, conn):
    findings = []
    # Group flows by terminal_sys_id
    by_terminal = flows_df[flows_df['terminal_sys_id'].notna()].groupby('terminal_sys_id')
    for terminal_id, group in by_terminal:
        # Find distinct root Exp nodes reaching this terminal
        distinct_roots = group['root_exp_id'].unique()
        if len(distinct_roots) < 2:
            continue
        for i in range(len(distinct_roots)):
            for j in range(i+1, len(distinct_roots)):
                root_a = distinct_roots[i]
                root_b = distinct_roots[j]
                # Version check: skip if same lineage
                if same_version_lineage(root_a, root_b, conn):
                    continue
                # Get representative paths
                path_a = group[group['root_exp_id'] == root_a].iloc[0]['node_path']
                path_b = group[group['root_exp_id'] == root_b].iloc[0]['node_path']
                all_nodes = list(set(path_a + path_b))
                findings.append({
                    'pattern_type': 'DUPLICATE_FLOW',
                    'node_ids':     all_nodes,
                    'severity':     'HIGH',
                    'detail': {
                        'terminal_node': get_name(terminal_id, conn),
                        'flow_a': [get_name(n, conn) for n in path_a],
                        'flow_b': [get_name(n, conn) for n in path_b],
                    }
                })
    return findings
```

### 5.2 PASS_THROUGH_HOP

A Proc node has exactly one outbound edge and performs no orchestration.
The Exp caller could call the Sys target directly.

```python
def find_pass_through_hops(G, id_to_name):
    findings = []
    for node_id in G.nodes:
        node = G.nodes[node_id]
        if node.get('layer') != 'proc':
            continue
        if G.out_degree(node_id) != 1:
            continue
        callee_id = list(G.successors(node_id))[0]
        callers   = list(G.predecessors(node_id))
        findings.append({
            'pattern_type': 'PASS_THROUGH_HOP',
            'node_ids':     [node_id, callee_id] + callers,
            'severity':     'MEDIUM',
            'detail': {
                'proc_node':  id_to_name[node_id],
                'only_calls': id_to_name[callee_id],
                'called_by':  [id_to_name[c] for c in callers],
            }
        })
    return findings
```

### 5.3 DEEP_CHAIN

A materialised flow has 4 or more hops, indicating possible unnecessary
intermediate steps.

```python
DEEP_CHAIN_THRESHOLD = 4   # tune upward if too many false positives

def find_deep_chains(flows_df, id_to_name):
    deep = flows_df[flows_df['hop_count'] >= DEEP_CHAIN_THRESHOLD].copy()
    findings = []
    for _, row in deep.iterrows():
        findings.append({
            'pattern_type': 'DEEP_CHAIN',
            'node_ids':     row['node_path'],
            'severity':     'LOW' if row['hop_count'] == 4 else 'MEDIUM',
            'detail': {
                'hop_count': row['hop_count'],
                'path':      [id_to_name.get(n) for n in row['node_path']],
            }
        })
    return findings
```

### 5.4 FAN_IN_CLUSTER

A Sys node is called by 3 or more different Proc nodes, indicating either
healthy high-value shared asset or accidental convergence worth reviewing.

```python
FAN_IN_THRESHOLD = 3   # raise to 5 at full 700-node scale if too noisy

def find_fan_in_clusters(G, id_to_name):
    findings = []
    for node_id in G.nodes:
        if G.nodes[node_id].get('layer') != 'sys':
            continue
        proc_callers = [p for p in G.predecessors(node_id)
                        if G.nodes[p].get('layer') == 'proc']
        if len(proc_callers) < FAN_IN_THRESHOLD:
            continue
        findings.append({
            'pattern_type': 'FAN_IN_CLUSTER',
            'node_ids':     [node_id] + proc_callers,
            'severity':     'LOW',
            'detail': {
                'sys_node':  id_to_name[node_id],
                'in_degree': len(proc_callers),
                'callers':   [id_to_name[c] for c in proc_callers],
            }
        })
    return findings
```

### 5.5 Structural score for merge candidates

When a DUPLICATE_FLOW finding is raised, a `merge_candidates` row is
created immediately with a structural score only. LLM rationale is added
in the semantic detection phase.

```python
def structural_score(flow_a_len, flow_b_len, same_domain: bool) -> float:
    """Simple structural confidence score for a duplicate flow pair."""
    length_similarity = 1.0 - abs(flow_a_len - flow_b_len) / max(flow_a_len, flow_b_len)
    domain_bonus      = 0.10 if same_domain else 0.0
    return round(min(1.0, 0.70 + (length_similarity * 0.20) + domain_bonus), 4)
```

---

## 6. Open decisions

- `DEEP_CHAIN_THRESHOLD = 4` — raise if findings are too noisy at full scale
- `FAN_IN_THRESHOLD = 3` — raise to 5 at 700+ node scale
- `traffic_metrics` is optional; platform functions correctly without it
- `merge_candidates` structural score is preliminary — final scoring happens
  in the semantic detection phase when LLM rationale is added
