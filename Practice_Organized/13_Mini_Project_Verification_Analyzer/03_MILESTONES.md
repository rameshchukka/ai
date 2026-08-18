# Milestones — Kibana Log Verification Engine (Phase 1 + Phase 2)

25 milestones total: **M0–M12 (Phase 1 — Log Verification Engine)** and **M13–M24 (Phase 2 —
Distributed Transaction Statistics & Performance Analyzer)**. Each is scoped to be completable
and verifiable in one agent session. Each maps to specific section(s) of a requirements doc —
Phase 1 milestones reference `REQUIREMENTS.md` (section numbers like "3.1"), Phase 2 milestones
reference `REQUIREMENTS_PHASE2.md` (prefixed "P2 §" below to avoid confusion with Phase 1 section
numbers, since both docs number sections independently starting from 1).
**Do not implement a milestone's listed "Explicitly out of scope" items early** — later milestones
depend on those being absent so far, and pulling them forward breaks the verification model.

**Phase boundary:** Phase 2 (M13–M24) must not start until Phase 1 (M0–M12) is fully Complete.
Phase 2 SRS is explicit: *"No log parsing, timestamp parsing, or rule qualification shall occur in
this phase"* — every Phase 2 milestone reads from the Phase 1 `LogRepository` only, via the
interface documented in Phase 1's M12 (`PHASE2_INTERFACE.md` / `ARCHITECTURE.md` ADR-12). If a
Phase 2 milestone finds itself wanting to re-parse, re-timestamp, or re-qualify raw logs, that's a
sign something is being done in the wrong phase — stop and flag it rather than working around it.

---

### M0 — Project Foundation & Scaffolding
**SRS refs:** none directly (enables everything else); NFR "every module independently testable."
**Goal:** A running Flask app with the structure from `ARCHITECTURE.md`, empty blueprints, base
template with nav, test framework wired up, logging configured.
**Deliverables:**
- `app/__init__.py` (`create_app()`), 4 empty blueprints registered, `run.py`.
- `base.html` with Bootstrap + htmx CDN includes, top nav (items disabled per UI guard).
- `requirements.txt`, `pytest.ini`, one trivial passing test (health-check route).
- `tests/fixtures/` directory created (empty, ready for later milestones).
- Logging configured (console + rotating file).
**Explicitly out of scope:** any parsing, mapping, or rule logic.
**Definition of Done:** `flask run` serves a homepage with disabled nav items; `pytest` passes;
`PROJECT_STATUS.md` initialized.

---

### M1 — Field Mapping Configuration
**SRS refs:** 3.4, NFR "no hardcoded field names."
**Goal:** Configurable canonical-field-to-source-column mapping, loadable/savable as JSON.
**Deliverables:**
- `core/field_mapping/` — `FieldMap` model, validate(), load/save JSON presets.
- Field Mapping screen (UI_DESIGN Screen 2) wired to a stub "detected columns" list (real columns
  come from M2 — for now, accept a manually-entered or fixture column list so this milestone is
  testable standalone).
- Unit tests: valid mapping, missing required canonical field, duplicate source column, preset
  save/load round-trip.
**Explicitly out of scope:** real file upload (M2), using the mapping against actual data.
**DoD:** Can define, save, and reload a field mapping; all core/ modules elsewhere reference only
canonical names going forward.

---

### M2 — Log File Loading & Parsing
**SRS refs:** 3.1.
**Goal:** Upload a CSV or point to a local path; chunked parsing; configurable delimiter; UTF-8;
skip blank/malformed rows with a structured report; uses the M1 FieldMap to resolve columns.
**Deliverables:**
- `core/parser/` — generator-based chunked reader, delimiter option, `LoadReport`
  (total/loaded/skipped/errors with capped sample).
- Load screen (UI_DESIGN Screen 1) functional end to end against a real uploaded/local file.
- Fixture files in `tests/fixtures/`: clean CSV, CSV with blank rows, CSV with malformed rows,
  large synthetic CSV (thousands of rows) to sanity-check chunking.
- Unit + integration tests for all of the above.
**Explicitly out of scope:** timestamp parsing (raw timestamp strings pass through untouched),
correlation filtering, repository storage (rows are parsed but not yet persisted with internal
IDs — that's M5; for now the load report is enough to verify this milestone).
**DoD:** Loading any fixture file produces correct Total/Loaded/Skipped/Errors counts on screen.

---

### M3 — Timestamp Parsing & Validation
**SRS refs:** 3.2.
**Goal:** User selects one of the 4 supported formats; timestamps parsed, invalid ones rejected
and counted, normalized datetime stored alongside the preserved original string.
**Deliverables:**
- `core/timestamp/` — one strategy class per format + factory/registry.
- Timestamp half of Screen 3 (UI_DESIGN) wired up, operating on the rows loaded in M2.
- Unit tests per format (valid + invalid input for each), plus a mixed-validity fixture file.
**Explicitly out of scope:** correlation filtering, repository (still operating on the in-flight
row stream from M2, not yet a queryable store).
**DoD:** Selecting each of the 4 formats against the right fixture correctly parses/rejects; an
invalid-timestamp count surfaces on screen.

---

### M4 — Correlation ID Filtering
**SRS refs:** 3.3.
**Goal:** User supplies a correlation ID pattern (e.g. `SFDC*`); only matching records are kept
eligible, the rest are counted as ignored (not deleted, not silently dropped — counted).
**Clarification — load-test window & unique correlation IDs:** the uploaded log file *is* the
load-test time window (start to end) — there's no separate "period" input in Phase 1; whatever
time range the file covers is the range analyzed. An **empty/unset correlation pattern must mean
"match all"** (every unique Correlation ID in the file is eligible), not "match nothing" — the
pattern exists to let a user narrow the analysis (e.g. to one test's IDs mixed in a shared log),
not to require narrowing. This matters downstream: Phase 2's Transaction Builder (M15) only ever
sees whatever M4 marks eligible, so an overly-strict default here would silently drop correlation
IDs out of the entire load-test analysis.
**Deliverables:**
- `core/correlation/` — pattern matcher (glob-style `*` wildcard at minimum; note in
  `PROJECT_STATUS.md` if regex support is added). Empty pattern → all records eligible.
- Correlation half of Screen 3 wired up.
- Unit tests: full match, no match, partial/wildcard match, **empty pattern matches every unique
  Correlation ID present** (not zero).
**DoD:** Total Matching / Ignored counts on screen are correct against fixtures, including the
empty-pattern "matches everything" case.

---

### M5 — In-Memory Log Repository
**SRS refs:** Section 4.
**Goal:** Every record that survived M2–M4 gets a permanent, immutable internal ID and is stored
in the `LogRepository`. This is the first milestone where "load → repository" is a complete,
queryable pipeline.
**Deliverables:**
- `core/repository/` — `LogRecord` (frozen dataclass), `LogRepository` (`add`, `get_by_id`,
  `get_all`, `filter(**criteria)`, secondary indices per ADR-4).
- Wizard Step 3's "Apply" button now actually populates the repository end-to-end (load → map →
  timestamp → correlation → repository).
- Unit tests: ID immutability/uniqueness, sequential assignment, filter correctness, index
  rebuild correctness, large-N performance smoke test (not a perf benchmark, just "doesn't fall
  over" at a few hundred thousand synthetic rows).
**DoD:** After completing the 3-step wizard against a fixture file, `LogRepository.get_all()`
returns exactly the eligible records with correct, stable internal IDs.

---

### M6 — Rule Configuration & Condition Engine
**SRS refs:** Sections 5, 6, 7 (sample rules as test cases).
**Goal:** Define rules (JSON or text) with up to 5 conditions, 10 operators, AND/OR/NOT
combination — pure logic, no execution against real data yet.
**Deliverables:**
- `core/rules/` — `Operator` classes (all 10), `Condition`, `Rule`, `RuleConfigLoader` interface +
  `JsonRuleLoader` + `TextRuleLoader`.
- Rule Manager screen (UI_DESIGN Screen 4): create/edit/list/enable/disable/import rules. Field
  dropdown sourced from the active FieldMap's canonical names (ADR-3/ADR-7).
- Unit tests: each operator individually, AND/OR/NOT combination correctness, all 5 sample rules
  from Section 7 expressed and validated as data structures, malformed rule definitions rejected
  with a clear error (not a silent failure).
**Explicitly out of scope:** actually running rules against the repository (M7).
**DoD:** All 5 sample rules can be created via the UI or imported as JSON/text and are stored as
valid `Rule` objects; condition evaluation logic is fully unit-tested in isolation from Flask.

---

### M7 — Rule Execution Engine
**SRS refs:** Section 8.
**Goal:** Run all enabled rules against the M5 repository; each rule executes independently and
read-only; produce per-rule results.
**Deliverables:**
- `core/rules/engine.py` (or similar) — `RuleEngine.run(repository, rules) -> list[RuleResult]`,
  `RuleResult` = rule name, match count, execution time, matched internal IDs, matched correlation
  IDs.
- "Run All Rules" wired up on Screen 5 (top half — results table, not yet the detail view).
- Unit tests: rules never mutate repository records (assert before/after equality), independent
  execution (one rule's match doesn't affect another), correct counts against the Section 7
  sample rules run on a known fixture dataset, execution-time field is populated and non-negative.
**DoD:** Running all 5 sample rules against a fixture dataset produces the exact expected match
counts and IDs, verified by test, and the summary table renders correctly.

---

### M8 — Rule Result UI (detail view)
**SRS refs:** Section 9.
**Goal:** Selecting a rule shows only its matching records, with exactly the specified columns.
**Deliverables:**
- Rule Result detail screen (UI_DESIGN Screen 5, bottom half), paginated via htmx.
- Columns exactly: Internal Log ID, Timestamp, Correlation ID, Application, API, Message,
  Payload, Elapsed, Log Level, expandable Complete Log.
- Sorting on every displayed column (Ascending/Descending, same convention as M9's Log Viewer —
  see M9 for the exact click-cycle and data-type-aware sort behavior; implement it consistently
  here rather than reinventing it).
- Integration tests: clicking through from results table to detail view returns only that rule's
  matched records, correct columns, sort correctness in both directions for at least the
  Timestamp and Elapsed columns, pagination works on a large match set.
**DoD:** For each of the 5 sample rules, the detail view shows exactly the matched records and no
others.

---

### M9 — Log Viewer
**SRS refs:** Section 10 (clarified: sorting shall be available on every displayed column,
supporting both Ascending and Descending — see "Sorting requirement" note below).
**Goal:** Browse all records (not just rule matches): show all / filter by rule, search, sort,
paginate, and a persisted (session-scoped) column selector.
**Deliverables:**
- Log Viewer screen (UI_DESIGN Screen 6).
- Column-selection checkboxes persisted via Flask session (ADR-9) — verify by reloading the page
  and confirming selection survived.
- **Sorting — every currently-displayed column is sortable, not just a subset.** Clicking a
  column header cycles Ascending → Descending → Ascending (indicated with an ↑/↓ arrow on the
  active sort column). Sorting is by one column at a time; selecting a new column to sort by
  resets that column to Ascending and clears the previous sort. Sorting must respect each
  column's actual data type, not just lexical string order — e.g. `Elapsed` sorts numerically,
  `Timestamp` sorts chronologically (using the normalized datetime from M3, not the raw preserved
  string). If the user hides a column via the column selector, it's no longer sortable from the
  header (it isn't displayed), but if they re-show it, it becomes sortable again — the column
  selector and the sort controls stay in sync.
- Pagination, "Filter by Rule" dropdown reusing M7/M8's rule results.
- Integration tests: sort correctness in **both directions for every column** (string, numeric,
  and timestamp columns each get an explicit ascending + descending test), sort state resets
  correctly when switching sort column, pagination boundaries (first/last page, partial last
  page), column persistence across requests within a session, "Filter by Rule" matches M8's
  output exactly.
**Explicitly out of scope:** the full multi-field filter panel (M10) — basic free-text search only
here.
**Note for M8:** the Rule Result detail screen (M8) displays a similar multi-column table. For UI
consistency, apply the same per-column Ascending/Descending sorting convention there if not
already done — if M8 was completed without it, log a deviation in `PROJECT_STATUS.md` and treat
adding it as a small follow-up task under this milestone rather than silently skipping it.

---

### M10 — Search & Filter Engine
**SRS refs:** Section 11.
**Goal:** Generalize filtering across every listed field, including ranges (Elapsed, Timestamp).
**Deliverables:**
- `core/search/` — query builder translating the filter panel's inputs into
  `LogRepository.filter(**criteria)` calls (extending the repository's filter capability with
  range and multi-value support as needed).
- Search & Filter panel (UI_DESIGN) wired into the Log Viewer.
- Unit tests: each filterable field individually, combined filters (AND semantics across
  fields), range filters (Elapsed >, Timestamp between), empty/no-match cases.
**DoD:** Every field listed in Section 11 is independently filterable and combinable, verified by
test against a fixture dataset with known expected matches.

---

### M11 — Verification Summary
**SRS refs:** Section 12.
**Goal:** A single dashboard aggregating the counts already produced by M2–M7.
**Deliverables:**
- Summary screen (UI_DESIGN Screen 7) — Total/Eligible/Ignored/Invalid/Loaded Records, Rules
  Executed, Total Rule Matches, Rule Failures, Processing Time.
- This milestone should **not** introduce new counting logic — it aggregates numbers already
  computed and tested in earlier milestones (LoadReport, correlation counts, RuleResult list).
  If a number isn't available from an earlier milestone's output, that's a sign an earlier
  milestone's deliverable was incomplete — flag it in `PROJECT_STATUS.md` rather than inventing a
  new ad-hoc calculation here.
- Integration test: summary numbers match the sum/values of the underlying reports exactly, for a
  known fixture run end to end.

---

### M12 — Non-Functional Hardening & Phase 2 Readiness
**SRS refs:** Section 13 (remaining items), Section 14.
**Goal:** Close out the non-functional requirements not already covered, and make sure the
Phase 1 → Phase 2 handoff boundary (ADR-12) is real and documented.
**Deliverables:**
- Large-file pass: run the full wizard + rule execution against a generated multi-hundred-
  thousand-row (or larger, hardware permitting) fixture; confirm memory stays bounded and chunked
  loading is actually chunking (add a test/log assertion, not just an eyeball check).
- A short `PHASE2_INTERFACE.md` (or section in `ARCHITECTURE.md`) documenting exactly which
  `LogRepository` / `RuleResult` methods Phase 2 is expected to consume — the "single source of
  truth" contract made explicit and reviewable.
- Full regression pass: every milestone's test suite green together, not just individually.
- Any remaining "no hardcoded field names" / "parser independent of Kibana version" /
  "rules independent of log template" claims spot-checked with a test that swaps in a
  differently-shaped fixture file + field mapping and confirms everything still works unmodified.
**DoD:** Full test suite green, large-file run completes without unbounded memory growth, Phase 2
interface documented. This milestone closes Phase 1.

---

# Phase 2 — Distributed Transaction Statistics & Performance Analyzer (M13–M24)

## Design notes (pending formal ADR additions to ARCHITECTURE.md)

These aren't yet written up as ADRs in `ARCHITECTURE.md` — that file wasn't part of this update.
They're flagged here so milestones M13+ are still self-sufficient. Recommend formalizing as
ADR-13 onward when `ARCHITECTURE.md` is next revised.

1. **Reuse the Phase 1 Condition/Operator engine for API Indicators.** An "Entry Indicator" /
   "Exit Indicator" / "Error Indicator" (P2 §4) is structurally identical to a Phase 1 rule
   Condition — field + operator + value (e.g. `Message Contains "Customer Request"`). Build on
   `core/rules`'s existing Condition/Operator classes rather than writing a second matcher.
2. **One shared statistics utility, used by both API-level and end-to-end stats.** Min/max/avg/
   median/P90/P95/P99/stddev (P2 §7, §8) should be computed by a single `core/stats/` helper, not
   reimplemented per milestone — and the percentile method (nearest-rank vs. linear
   interpolation) must be explicitly chosen and tested, since "P95" is ambiguous without one.
3. **One shared Top-N ranking utility** backs both Slowest and Fastest Transactions (P2 §11, §12)
   — same function, opposite sort direction, not two copies.
4. **One shared table macro** (Jinja2) for sort/paginate/search/export, used by every Phase 2 tab
   (P2 §15) — built once in M24, not duplicated nine times across tabs.
5. **New dependency:** `openpyxl` for Excel export (P2 §16). Add to `requirements.txt` in M24.
6. **Phase 2 introduces no new persistent storage.** Transactions, matched entry/exit/error
   records, and computed statistics are derived, in-memory structures rebuilt from the Phase 1
   repository on demand (or cached per session) — never a second source of truth.

---

### M13 — Phase 2 Foundation: Repository Integration & Tab Shell
**SRS refs:** P2 §1, §2, §3 (Processing Flow), §15 (tab shell only).
**Goal:** Stand up Phase 2's Flask blueprint(s) consuming the Phase 1 `LogRepository` read-only,
plus the 9-tab navigation shell (Summary, API Statistics, End-to-End Statistics, Missing
Correlations, Errors, Slowest Transactions, Fastest Transactions, Transaction Explorer, Export)
with placeholder content per tab.
**Deliverables:**
- New blueprint(s) (e.g. `analytics`) registered into the existing app factory alongside Phase 1's
  four blueprints.
- A test that explicitly asserts Phase 2 code imports/uses only `LogRepository`'s public methods
  (per Phase 1 ADR-12) and does not import Phase 1's parser/timestamp/rules internals directly —
  enforces "no log parsing, timestamp parsing, or rule qualification" at the code-structure level,
  not just by convention.
- Tab shell UI per `UI_DESIGN.md`'s Phase 2 site map, each tab a stub for now.
- Smoke tests: every tab route returns 200 with placeholder content.
**Explicitly out of scope:** any real statistics computation — every tab is a stub until later
milestones fill it in.
**DoD:** Navigation between the Phase 1 wizard and all 9 Phase 2 tabs works; a test proves Phase 2
reads only from the verified repository.

---

### M14 — API Configuration
**SRS refs:** P2 §4.
**Goal:** Configure up to 4 APIs, each with a Name and Entry/Exit/Error Indicator.
**Deliverables:**
- `core/api_config/` — `ApiConfig` model (name + 3 indicators, each an Indicator reusing Phase 1's
  Condition/Operator classes per Design Note 1), validation (max 4 APIs, each indicator
  well-formed).
- API Configuration screen (`UI_DESIGN.md` Phase 2 section).
- JSON save/load of named API-config presets, mirroring Phase 1's FieldMap preset pattern (M1).
- Unit tests: valid config, a 5th API rejected, malformed indicator rejected with a clear error,
  preset save/load round-trip.
**Explicitly out of scope:** applying these indicators against real records (M16).
**DoD:** Up to 4 APIs configurable with working Entry/Exit/Error indicators, stored as validated,
reloadable config.

---

### M15 — Transaction Builder
**SRS refs:** P2 §5.
**Goal:** Group `LogRepository` records by Correlation ID and order each group chronologically —
the ordered substrate every later Phase 2 milestone operates on. This milestone does **not**
classify events as entry/exit/error yet.
**Clarification — coverage:** this must group **every unique Correlation ID present in the
repository**, with no additional filtering of its own. The repository already represents exactly
the load-test window the user uploaded (Phase 1 M2) and whichever Correlation IDs M4 marked
eligible (default: all of them, per M4's clarification) — Transaction Builder's job is to
organize that complete set into per-transaction event sequences, not to narrow it further.
**Deliverables:**
- `core/transactions/builder.py` — `build_transactions(repository) -> dict[correlation_id,
  list[LogRecord]]`, ordered by the Phase 1 M3 normalized timestamp (never the raw preserved
  string).
- A documented, tested tie-break rule for same-timestamp events (e.g. stable by `internal_id`).
- Unit tests: grouping correctness, chronological ordering correctness including the tie-break
  case, single-record and empty correlation groups handled without error.
**Explicitly out of scope:** API-specific entry/exit/error matching and completeness validation
(M16).
**DoD:** Given a fixture repository, transactions are grouped and ordered exactly as expected.

---

### M16 — API Entry/Exit/Error Matching
**SRS refs:** P2 §6.
**Goal:** For each configured API (M14) applied to each transaction (M15), determine Entry/Exit/
Error records, Entry/Exit timestamps, API elapsed time, and status — plus the listed validations.
**Deliverables:**
- `core/transactions/matching.py` — applies an API's indicators to a transaction's ordered events;
  produces a documented status enum (e.g. Success / Failed / Error / Incomplete).
- Validations implemented exactly as listed in P2 §6: single entry, single exit-or-error, exit
  after entry. Each violation is classified using a **shared anomaly vocabulary** that M20 (Missing
  Correlation Analysis) reuses directly rather than re-deriving.
- Unit tests covering every case: clean single entry/exit, missing entry, missing exit, duplicate
  entry, duplicate exit, error-only, exit-before-entry (must be flagged, never silently accepted).
**Explicitly out of scope:** aggregate statistics — TPS, response-time percentiles (M17).
**DoD:** Given fixture transactions with known anomalies, matching correctly classifies every case
listed in P2 §6.

---

### M17 — API Statistics Engine
**SRS refs:** P2 §7.
**Goal:** Per-API aggregates: transaction/entry/exit/error counts, success/failure counts, missing
and duplicate entry/exit counts, TPS (incoming/outgoing/peak/average, per-second and per-minute),
and response-time stats (min/max/avg/median/P90/P95/P99/stddev).
**Deliverables:**
- `core/stats/` shared percentile/stddev utility per Design Note 2 — explicitly document and test
  the percentile method chosen.
- `core/stats/api_stats.py` computing the full P2 §7 list per configured API from M16's output.
- TPS bucketing explicitly documented and tested: how "per second"/"per minute" windows are
  formed (e.g. floor entry timestamp to the second/minute), how Peak (max bucket count) differs
  from Average (mean bucket count over the observed range).
- Unit tests: each statistic individually against a hand-computed fixture, with percentile values
  verified against the documented method on a small known dataset.
**Explicitly out of scope:** cross-API end-to-end statistics (M18); polished UI (M24 handles
cross-cutting sort/paginate/search/export — this milestone's own tab can be a minimal table).
**DoD:** All P2 §7 metrics computed correctly per API against a fixture with known expected
values.

---

### M18 — End-to-End Statistics
**SRS refs:** P2 §8.
**Goal:** Per-completed-transaction Start (first API entry) / End (last API exit) and elapsed
time, using the same percentile/stddev suite as M17 but across the whole transaction, plus a
success/failure summary.
**Deliverables:**
- `core/stats/e2e_stats.py`, reusing M17's shared percentile utility (Design Note 2) — not a
  second implementation.
- An explicit, tested definition of "completed transaction" (e.g. at least one matched entry and
  one matched exit across the configured APIs) — P2 §8 assumes this without defining it, so this
  milestone must.
- Unit tests against a fixture mixing complete and incomplete transactions: incomplete ones are
  excluded from end-to-end stats but still accounted for elsewhere (cross-check against M20's
  count, don't let a transaction silently disappear from both).
**DoD:** End-to-end min/max/avg/median/P90/P95/P99/stddev and success/failure summary match
hand-computed fixture expectations.

---

### M19 — Error Statistics
**SRS refs:** P2 §9.
**Goal:** Aggregate error counts/percentages per API, top error messages, error distribution by
API, and a per-error detail table.
**Deliverables:**
- `core/stats/error_stats.py` consuming M16's error-classified records — no re-deriving error
  detection logic.
- Errors tab: Correlation ID, API, Timestamp, Error Indicator, Error Message columns (basic
  sort/paginate/search for now; M24 polishes this to the shared convention).
- Unit tests: error counts/percentages, "top error messages" ranking with a documented tie-break,
  per-API error distribution.
**DoD:** Error statistics and the error detail table match fixture expectations exactly.

---

### M20 — Missing Correlation Analysis
**SRS refs:** P2 §10.
**Goal:** Surface every anomaly M16 already classified (missing entry/exit/intermediate API,
duplicate entry/exit, incomplete transaction) as a dedicated report — no new detection logic.
**Deliverables:**
- `core/stats/missing_correlation.py`, reusing M16's shared anomaly vocabulary directly.
- Missing Correlations tab: Correlation ID, API, Missing Component, Remarks columns.
- Unit tests: every anomaly type listed in P2 §10 represented in a fixture and correctly reported,
  cross-checked against M18's "completed transaction" accounting so nothing silently disappears.
**DoD:** Every anomaly type listed in P2 §10 is detected and displayed correctly.

---

### M21 — Slowest & Fastest Transactions
**SRS refs:** P2 §11, §12.
**Goal:** Configurable Top-N (default 20) slowest and fastest transactions by elapsed time, with
sorting.
**Deliverables:**
- One shared ranking utility (Design Note 3) taking M18's per-transaction elapsed times and a
  configurable N — Fastest = ascending, Slowest = descending, same function, opposite direction.
- Two tabs (Slowest / Fastest): Rank, Correlation ID, API, Entry Time, Exit Time, Elapsed Time
  columns, sortable per the Phase 1 M9 convention.
- Unit tests: Top-N correctness, N larger than available transactions handled gracefully, a
  documented tie-break rule when elapsed times are equal (e.g. stable by Correlation ID).
**DoD:** Slowest/Fastest tabs show correct Top-N results with working configurable N and sorting.

---

### M22 — Transaction Explorer
**SRS refs:** P2 §13.
**Goal:** Search by Correlation ID; show the complete event timeline, API sequence, entry/exit
timestamps, elapsed time, and transaction status, sorted chronologically.
**Deliverables:**
- Transaction Explorer tab per `UI_DESIGN.md`'s Phase 2 wireframe.
- Reuses M15's transaction builder output directly — no new grouping/ordering logic.
- Integration tests: a known Correlation ID returns the exact expected timeline; an unknown ID
  produces a clear "not found" state, not an error page.
**DoD:** Any Correlation ID present in the repository can be explored with a correct chronological
timeline.

---

### M23 — Summary Dashboard
**SRS refs:** P2 §14.
**Goal:** A consolidated cross-API table (Entries/Exits/Errors/Incoming TPS/Outgoing TPS/Average/
P95/P99 for up to 4 APIs) plus an Overall Summary (Total Transactions, Average/P95/P99
End-to-End, Success Rate, Failure Rate).
**Deliverables:**
- Summary tab assembling numbers **already computed** in M17 (API stats) and M18 (end-to-end
  stats) — same rule as Phase 1's M11: no new counting logic invented here. If a required number
  isn't available from M17/M18's output, that means those milestones need a small addition —
  flag it, don't patch around it here.
- Integration test: summary values match M17/M18's outputs exactly, for 1, 2, and 4 configured
  APIs (boundary cases).
**DoD:** Summary dashboard renders correctly for 1, 2, and 4 configured APIs against fixtures.

---

### M24 — Cross-Cutting UI Polish: Sorting, Pagination, Search & Export
**SRS refs:** P2 §15, §16 (also finalizes the "support sorting" notes left as "basic for now" in
M19/M21).
**Goal:** Every Phase 2 table, across all 9 tabs, supports sorting on every column (ascending/
descending, same convention as Phase 1's M9), pagination, search, and export to CSV and Excel.
**Deliverables:**
- One shared table-rendering macro (Design Note 4) used by every Phase 2 tab — replacing any
  per-tab ad hoc sort/paginate/search built during M17–M23's stub phase.
- Export: CSV via stdlib `csv`; Excel via `openpyxl` (new dependency, Design Note 5 — add to
  `requirements.txt`).
- Integration tests on at least 3 representative tabs (e.g. API Statistics, Slowest Transactions,
  Error Statistics): sort (every column, both directions), paginate, search, and export all work,
  and exported file content matches what's on screen.
**DoD:** Every tab listed in P2 §15 has working sort on every column in both directions,
pagination, search, and export to both CSV and Excel. This milestone closes Phase 2.

---

## Milestone summary table

| ID | Name | SRS refs | Depends on |
|---|---|---|---|
| M0 | Project Foundation & Scaffolding | — | — |
| M1 | Field Mapping Configuration | 3.4 | M0 |
| M2 | Log File Loading & Parsing | 3.1 | M0, M1 |
| M3 | Timestamp Parsing & Validation | 3.2 | M2 |
| M4 | Correlation ID Filtering | 3.3 | M2 |
| M5 | In-Memory Log Repository | 4 | M2, M3, M4 |
| M6 | Rule Configuration & Condition Engine | 5, 6, 7 | M1 |
| M7 | Rule Execution Engine | 8 | M5, M6 |
| M8 | Rule Result UI | 9 | M7 |
| M9 | Log Viewer | 10 | M5 |
| M10 | Search & Filter Engine | 11 | M5, M9 |
| M11 | Verification Summary | 12 | M2, M4, M7 |
| M12 | Non-Functional Hardening & Phase 2 Readiness | 13, 14 | all (Phase 1) |
| M13 | Phase 2 Foundation: Repository Integration & Tab Shell | P2 §1,2,3,15 | M12 |
| M14 | API Configuration | P2 §4 | M13 |
| M15 | Transaction Builder | P2 §5 | M13 |
| M16 | API Entry/Exit/Error Matching | P2 §6 | M14, M15 |
| M17 | API Statistics Engine | P2 §7 | M16 |
| M18 | End-to-End Statistics | P2 §8 | M16, M17 |
| M19 | Error Statistics | P2 §9 | M16 |
| M20 | Missing Correlation Analysis | P2 §10 | M16, M18 |
| M21 | Slowest & Fastest Transactions | P2 §11, §12 | M18 |
| M22 | Transaction Explorer | P2 §13 | M15 |
| M23 | Summary Dashboard | P2 §14 | M17, M18 |
| M24 | Cross-Cutting UI Polish: Sorting, Pagination, Search & Export | P2 §15, §16 | M17–M23 |
