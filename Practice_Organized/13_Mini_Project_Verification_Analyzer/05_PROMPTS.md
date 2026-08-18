# Milestone Prompts — Kibana Log Verification Engine (Phase 1 + Phase 2)

One ready-to-paste prompt per milestone. Use them **in order**, one per fresh agent session.
Every prompt follows the same shape on purpose — the agent should never be guessing what "done"
means.

Assumes the repo root contains: `REQUIREMENTS.md` (Phase 1 SRS), `REQUIREMENTS_PHASE2.md` (Phase
2 SRS — rename the uploaded `Log_Statistics.txt`), `ARCHITECTURE.md`, `UI_DESIGN.md`,
`MILESTONES.md`, `PROJECT_STATUS.md` (rename the uploaded files to drop the numeric prefixes, or
adjust the filenames in the prompts below to match whatever you actually used).

M0–M12 below are Phase 1. M13–M24 are Phase 2 — **do not run the M13 prompt until M12 is marked
Complete in `PROJECT_STATUS.md`**; Phase 2 depends on the finished, verified Phase 1 repository
and its documented interface.

---

## Master template (for reference / writing new milestones later, e.g. Phase 2)

```
You are continuing the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full, especially "Context for Next Agent Session."
2. Read MILESTONES.md, section "M<N> — <name>" only.
3. Read ARCHITECTURE.md in full if you haven't internalized it this session — it's the binding
   set of design decisions; don't re-derive or contradict it without logging a deviation.
4. Read UI_DESIGN.md, section(s) relevant to this milestone, if this milestone touches the UI.
5. Read REQUIREMENTS.md, section(s): <SRS refs for this milestone>.

Scope: implement ONLY M<N> as defined in MILESTONES.md. Do not implement features listed under
later milestones, even if they seem trivial to add while you're in the relevant file. Do not
modify code from a previously-completed milestone unless you find a genuine regression — if you
do, fix it and log it under "Deviations" in PROJECT_STATUS.md with the reason.

Tasks:
- Implement the deliverables listed for M<N>.
- Write unit/integration tests per the "Deliverables" and "DoD" in MILESTONES.md for M<N>.
- Run the FULL test suite (not just new tests) and confirm everything passes — this is your
  regression check against every previously completed milestone.

Before stopping:
- Update PROJECT_STATUS.md: mark M<N> Complete with today's date, update the File/Module
  Inventory, update Test Status with the full-suite results, write a fresh "Context for Next
  Agent Session" note, set Current Milestone to M<N+1>, log any new architecture decisions or
  deviations.
- Report clearly: "Milestone M<N> complete" or "Milestone M<N> blocked because: <reason>" — do
  not silently move on to M<N+1>.
```

---

## M0 — Project Foundation & Scaffolding

```
You are starting the Kibana Log Verification Engine build from scratch.

1. Read PROJECT_STATUS.md (it should say nothing has been built yet — confirm that).
2. Read MILESTONES.md, section "M0 — Project Foundation & Scaffolding."
3. Read ARCHITECTURE.md in full — this is the binding set of design decisions for the whole
   project (app structure, tech stack, patterns). Internalize the "Project structure" tree.
4. Skim UI_DESIGN.md for the overall site map and base-layout expectations (nav items, disabled
   state before data is loaded).

Scope: ONLY scaffolding. No parsing, mapping, or rule logic — those are later milestones.

Tasks:
- Set up the project structure exactly as shown in ARCHITECTURE.md's "Project structure" tree
  (empty/stub modules where listed; you don't need to pre-create every file, but the directory
  layout should match).
- Implement create_app() (Flask app factory) with the 4 blueprints (upload, rules, viewer,
  summary) registered, each with a trivial placeholder route for now.
- Implement base.html with Bootstrap 5 + htmx via CDN, and a top nav matching UI_DESIGN.md's site
  map, with nav items disabled per the "wizard guard" note until told otherwise (hardcode disabled
  for now — real gating logic comes later).
- Set up requirements.txt, pytest.ini, and logging (console + rotating file handler) per
  ARCHITECTURE.md.
- Write one trivial passing test (e.g. homepage returns 200).
- Create the tests/fixtures/ directory (empty, ready for future milestones to populate).

Before stopping:
- Confirm `flask run` serves a homepage with the nav visible (disabled) and `pytest` passes.
- Update PROJECT_STATUS.md per the standard close-out (mark M0 Complete, fill File/Module
  Inventory, Test Status, write the "Context for Next Agent Session" note, set Current Milestone
  to M1).
- Report: "Milestone M0 complete" or describe what's blocking it.
```

---

## M1 — Field Mapping Configuration

```
Continuing the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full, especially "Context for Next Agent Session" — confirm M0 is
   marked Complete before proceeding.
2. Read MILESTONES.md, section "M1 — Field Mapping Configuration."
3. Read ARCHITECTURE.md's ADR-3 (configuration-driven field mapping) — this is the binding design
   for this milestone.
4. Read UI_DESIGN.md, "Screen 2 — Field Mapping."
5. Read REQUIREMENTS.md, section 3.4, and the NFR list in section 13 (note: "no hardcoded field
   names" applies starting now and for the rest of the project).

Scope: ONLY field mapping configuration. Do not implement real file upload (that's M2) — for this
milestone, accept a manually-entered or fixture-provided list of "detected columns" so the
feature is testable standalone.

Tasks:
- Implement core/field_mapping/: FieldMap model, validation (missing required canonical field,
  duplicate source column mapping), JSON save/load of named presets.
- Implement the Field Mapping screen per UI_DESIGN.md Screen 2, using a stub/fixture column list.
- Write unit tests: valid mapping, validation failure cases, preset save/load round-trip.
- Run the FULL test suite (including M0's) and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out (mark M1 Complete, update inventory/tests/
  context note, set Current Milestone to M2). Log any deviation if you had to interpret an
  ambiguous mapping rule.
- Report: "Milestone M1 complete" or describe what's blocking it.
```

---

## M2 — Log File Loading & Parsing

```
Continuing the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M1 is Complete.
2. Read MILESTONES.md, section "M2 — Log File Loading & Parsing."
3. Read ARCHITECTURE.md's ADR-5 (chunked/generator parsing) and ADR-10 (structured error/skip
   handling).
4. Read UI_DESIGN.md, "Screen 1 — Load Log File."
5. Read REQUIREMENTS.md, section 3.1.

Scope: ONLY file loading and parsing using the M1 FieldMap to resolve columns. Do not implement
timestamp parsing (raw timestamp strings pass through as-is), correlation filtering, or
repository storage with internal IDs — those are M3/M4/M5.

Tasks:
- Implement core/parser/: chunked/generator CSV reader, configurable delimiter, UTF-8, skip
  blank/malformed rows, LoadReport (total/loaded/skipped/errors with a capped error sample).
- Wire the Load screen (UI_DESIGN Screen 1) to support both CSV upload and local file path, using
  the active FieldMap from M1 to resolve which columns matter.
- Create fixture files under tests/fixtures/: a clean CSV, a CSV with blank rows, a CSV with
  malformed rows, and a larger synthetic CSV (a few thousand rows) to sanity-check chunking
  actually chunks (not just "works on a small file").
- Write unit + integration tests covering all of the above, including the on-screen
  Total/Loaded/Skipped/Errors counts.
- Run the FULL test suite and confirm everything passes (M0 and M1 included).

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M3.
- Report: "Milestone M2 complete" or describe what's blocking it.
```

---

## M3 — Timestamp Parsing & Validation

```
Continuing the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M2 is Complete.
2. Read MILESTONES.md, section "M3 — Timestamp Parsing & Validation."
3. Read ARCHITECTURE.md's ADR-6 (strategy pattern per timestamp format).
4. Read UI_DESIGN.md, "Screen 3," timestamp half only.
5. Read REQUIREMENTS.md, section 3.2.

Scope: ONLY timestamp parsing, operating on the row stream from M2. Do not implement correlation
filtering or repository storage yet (M4/M5).

Tasks:
- Implement core/timestamp/: one parser class per supported format (the 4 listed in REQUIREMENTS
  3.2) plus a factory/registry keyed by format name.
- Wire the timestamp half of Screen 3: user selects a format, timestamps parse, invalid ones are
  rejected and counted, normalized datetime is stored alongside the preserved original string.
- Add a mixed-validity fixture file (some valid, some invalid timestamps) plus per-format unit
  tests (valid + invalid input for each of the 4 formats).
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M4.
- Report: "Milestone M3 complete" or describe what's blocking it.
```

---

## M4 — Correlation ID Filtering

```
Continuing the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M3 is Complete.
2. Read MILESTONES.md, section "M4 — Correlation ID Filtering."
3. Read UI_DESIGN.md, "Screen 3," correlation half only.
4. Read REQUIREMENTS.md, section 3.3.

Scope: ONLY correlation ID pattern filtering. Do not implement repository storage with internal
IDs yet (M5).

Tasks:
- Implement core/correlation/: pattern matcher supporting at least glob-style wildcards (e.g.
  "SFDC*"). If you add regex support beyond what's needed, note that as a deviation/decision in
  PROJECT_STATUS.md rather than silently expanding scope.
- Wire the correlation half of Screen 3: records not matching the pattern are counted as ignored,
  not deleted or hidden from the count.
- Write unit tests: full match, no match, wildcard match, empty-pattern behavior (decide and
  document what empty pattern means — match all, or require explicit pattern — and record that
  decision).
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M5.
- Report: "Milestone M4 complete" or describe what's blocking it.
```

---

## M5 — In-Memory Log Repository

```
Continuing the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M2, M3, M4 are all Complete.
2. Read MILESTONES.md, section "M5 — In-Memory Log Repository."
3. Read ARCHITECTURE.md's ADR-4 (repository pattern) and ADR-12 (Phase 2 boundary) carefully —
   this milestone establishes the project's central data structure.
4. Read REQUIREMENTS.md, section 4.

Scope: this is the milestone that wires M2+M3+M4 together into a real, queryable store. Do not
implement rule logic yet (M6/M7), and do not implement the Search/Filter UI yet (M9/M10) — just
the repository's own filter() capability needs to exist and be correct.

Tasks:
- Implement core/repository/: LogRecord (frozen dataclass: internal_id, normalized fields dict,
  parsed timestamp, preserved original timestamp string), LogRepository (add, get_by_id,
  get_all, filter(**criteria), secondary indices for fast filtering per ADR-4).
- Wire the wizard's Step 3 "Apply" action to run the full load → map → timestamp → correlation →
  repository pipeline end to end for the first time.
- Write unit tests: internal_id uniqueness and immutability, sequential assignment never reused,
  filter() correctness against known fixture data, index rebuild correctness, and a large-N smoke
  test (a few hundred thousand synthetic rows) confirming nothing falls over — this is not a
  performance benchmark, just a sanity check.
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M6. Make sure the
  "Context for Next Agent Session" note clearly states the LogRepository's public method
  signatures, since M6/M7/M9/M10 all build directly on it.
- Report: "Milestone M5 complete" or describe what's blocking it.
```

---

## M6 — Rule Configuration & Condition Engine

```
Continuing the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M1 and M5 are Complete (M6 depends on the FieldMap
   from M1 for field names, but is otherwise independent pure logic — it does not need M2-M5's
   loading pipeline to run, only their concepts).
2. Read MILESTONES.md, section "M6 — Rule Configuration & Condition Engine."
3. Read ARCHITECTURE.md's ADR-7 (composable conditions, no eval/exec) and ADR-8 (pluggable rule
   config loaders) carefully.
4. Read UI_DESIGN.md, "Screen 4 — Rule Manager."
5. Read REQUIREMENTS.md, sections 5, 6, and 7 (the 5 sample rules — these are your primary test
   cases).

Scope: ONLY rule definition and condition evaluation as pure logic + the management UI. Do NOT
run rules against the real repository yet — that's M7. Do NOT use eval()/exec() anywhere, even
for the Regex operator (compile and match, don't interpret as code).

Tasks:
- Implement core/rules/: all 10 Operator classes, Condition, Rule, RuleConfigLoader interface,
  JsonRuleLoader, TextRuleLoader. Stub (interface only, not implemented) a DatabaseRuleLoader per
  ADR-8's "Future: Database" note.
- Implement the Rule Manager screen: create/edit/list/enable/disable/import rules, with the field
  dropdown sourced from the active FieldMap's canonical names (never hardcoded).
- Express all 5 sample rules from REQUIREMENTS.md section 7 as data (via the UI or by importing
  JSON/text) and validate they parse into correct Rule objects.
- Write unit tests: every operator individually (true and false cases), AND/OR/NOT combination
  correctness, malformed rule definitions rejected with a clear error (not silently dropped).
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M7.
- Report: "Milestone M6 complete" or describe what's blocking it.
```

---

## M7 — Rule Execution Engine

```
Continuing the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M5 and M6 are Complete.
2. Read MILESTONES.md, section "M7 — Rule Execution Engine."
3. Read REQUIREMENTS.md, section 8.

Scope: ONLY running rules (from M6) against the repository (from M5) and producing results. Do
NOT implement the per-rule detail view yet (M8) — just the results summary table.

Tasks:
- Implement the RuleEngine: run(repository, rules) -> list[RuleResult], where RuleResult carries
  rule name, match count, execution time, matched internal IDs, matched correlation IDs.
- Wire "Run All Rules" on the Rule Results screen (top half — summary table only).
- Write unit tests proving: rules never mutate repository records (assert record equality before
  and after a run), rules execute independently (one rule's outcome can't affect another's),
  exact match counts/IDs against the 5 sample rules run on a known fixture dataset (build this
  fixture deliberately so you know the expected matches ahead of time), execution-time field is
  populated and non-negative.
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M8.
- Report: "Milestone M7 complete" or describe what's blocking it.
```

---

## M8 — Rule Result UI (detail view)

```
Continuing the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M7 is Complete.
2. Read MILESTONES.md, section "M8 — Rule Result UI."
3. Read UI_DESIGN.md, "Screen 5 — Rule Results," detail-view part.
4. Read REQUIREMENTS.md, section 9.

Scope: ONLY the per-rule detail view (clicking into a rule's matches from M7's summary table).

Tasks:
- Implement the Rule Result detail screen: exactly these columns — Internal Log ID, Timestamp,
  Correlation ID, Application, API, Message, Payload, Elapsed, Log Level — plus an expandable
  "Complete Log" per row.
- Paginate via htmx partial swap (large match sets should not render all at once).
- Write integration tests: clicking through from the summary table to a rule's detail view shows
  exactly that rule's matched records (no more, no fewer), correct columns, pagination behaves
  correctly at boundaries.
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M9.
- Report: "Milestone M8 complete" or describe what's blocking it.
```

---

## M9 — Log Viewer

```
Continuing the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M5 is Complete (M9 builds on the repository; M7/M8
   help but the core "show all records" path only needs M5).
2. Read MILESTONES.md, section "M9 — Log Viewer."
3. Read ARCHITECTURE.md's ADR-9 (session-scoped UI state).
4. Read UI_DESIGN.md, "Screen 6 — Log Viewer."
5. Read REQUIREMENTS.md, section 10.

Scope: Show All / Filter by Rule / basic free-text search / sort / paginate / persisted column
selector. Do NOT implement the full multi-field filter panel yet (M10) — basic free-text search
only here.

Tasks:
- Implement the Log Viewer screen per UI_DESIGN.md Screen 6.
- Implement the column-selection checkboxes, persisted via Flask session (ADR-9) — verify
  persistence by reloading the page mid-session and confirming the selection survived.
- Implement sortable columns (click header) and pagination.
- Implement "Filter by Rule," reusing M7/M8's rule result data so it matches exactly.
- Write integration tests: sort correctness, pagination boundary cases (first page, last page,
  partial last page), column-selection persistence across requests within a session, "Filter by
  Rule" output matches M8's detail view output exactly for the same rule.
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M10.
- Report: "Milestone M9 complete" or describe what's blocking it.
```

---

## M10 — Search & Filter Engine

```
Continuing the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M9 is Complete.
2. Read MILESTONES.md, section "M10 — Search & Filter Engine."
3. Read UI_DESIGN.md, "Search & Filter panel."
4. Read REQUIREMENTS.md, section 11.

Scope: generalize filtering across every field listed in section 11, including ranges
(Elapsed, Timestamp). Extend LogRepository.filter() as needed rather than bypassing it.

Tasks:
- Implement core/search/: a query builder translating filter-panel inputs into
  LogRepository.filter(**criteria) calls, adding range and multi-value support to the repository
  layer if it isn't there already (if you need to touch M5's repository code to add this, that's
  expected — just make sure M5's existing tests still pass and don't change its public method
  signatures gratuitously).
- Wire the Search & Filter panel into the Log Viewer.
- Write unit tests: each filterable field individually, combined filters (confirm AND semantics
  across fields), range filters (Elapsed greater-than, Timestamp between two values), and
  no-match/empty-result cases.
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M11. If you
  changed LogRepository's internals, note that clearly under Deviations even if behavior didn't
  change, so future sessions know to re-check that area.
- Report: "Milestone M10 complete" or describe what's blocking it.
```

---

## M11 — Verification Summary

```
Continuing the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M2, M4, M7 are Complete.
2. Read MILESTONES.md, section "M11 — Verification Summary."
3. Read UI_DESIGN.md, "Screen 7 — Verification Summary."
4. Read REQUIREMENTS.md, section 12.

Scope: aggregate numbers ALREADY produced by earlier milestones (LoadReport from M2, correlation
counts from M4, RuleResult list from M7). Do not invent new counting logic in this milestone — if
a required number isn't available from an earlier milestone's output, stop and report that as a
blocker (it likely means an earlier milestone's deliverable needs a small addition, which should
be logged and possibly require revisiting that milestone explicitly, not patched over here).

Tasks:
- Implement the Verification Summary screen with all the stat cards listed in REQUIREMENTS.md
  section 12.
- Write an integration test confirming the summary's numbers exactly match the underlying
  reports/results for a known fixture run end to end (Total Records, Eligible, Ignored, Invalid,
  Loaded, Rules Executed, Total Rule Matches, Rule Failures, Processing Time).
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M12.
- Report: "Milestone M11 complete" or describe what's blocking it (including if you hit the
  "number not available" case above).
```

---

## M12 — Non-Functional Hardening & Phase 2 Readiness

```
Continuing the Kibana Log Verification Engine build. This is the final milestone of Phase 1.

1. Read PROJECT_STATUS.md in full — confirm M0-M11 are all Complete.
2. Read MILESTONES.md, section "M12 — Non-Functional Hardening & Phase 2 Readiness."
3. Read ARCHITECTURE.md's ADR-12 (Phase 2 boundary) and the "NFR → design mapping" table.
4. Read REQUIREMENTS.md, section 13 (all remaining items) and section 14.

Scope: close out NFRs not already covered, and make the Phase 1 → Phase 2 handoff explicit. No
new functional features in this milestone.

Tasks:
- Run the full wizard + rule execution against a generated large fixture (several hundred
  thousand rows or more, hardware permitting). Confirm memory stays bounded and add a test or
  logged assertion that chunked loading is genuinely chunking (not just "ran without crashing").
- Write PHASE2_INTERFACE.md (or a new section in ARCHITECTURE.md) documenting exactly which
  LogRepository and RuleResult methods/fields Phase 2 is expected to consume. This is the
  "single source of truth" contract — make it concrete (method signatures, field names) and
  reviewable, not just a restatement of intent.
- Spot-check the three NFR claims that matter most for reuse: swap in a differently-shaped
  fixture file + a different field mapping, and confirm parsing/rules/repository all still work
  with zero code changes (only configuration changes). Add this as an actual test if it isn't
  one already.
- Run the FULL test suite across all 13 milestones together and confirm everything is green.

Before stopping:
- Update PROJECT_STATUS.md: mark M12 Complete, set Overall Progress to 13/13, and write a final
  "Context for Next Agent Session" note summarizing the project's state for whoever starts
  Phase 2.
- Report: "Phase 1 complete — all 13 milestones done" or describe what's blocking final closeout.
```

---

## M13 — Phase 2 Foundation: Repository Integration & Tab Shell

```
You are starting Phase 2 of the Kibana Log Verification Engine: the Distributed Transaction
Statistics & Performance Analyzer. Phase 1 (M0-M12) must be Complete before you proceed.

1. Read PROJECT_STATUS.md in full — confirm M12 is marked Complete. If it is not, STOP and report
   that Phase 2 cannot begin yet, rather than proceeding.
2. Read MILESTONES.md, the "Phase 2 — Design notes" block and section "M13 — Phase 2 Foundation:
   Repository Integration & Tab Shell."
3. Read ARCHITECTURE.md's ADR-12 (Phase 2 boundary) and, if it exists, PHASE2_INTERFACE.md from
   M12's closeout — this defines exactly what you're allowed to depend on from Phase 1.
4. Read UI_DESIGN.md, the "Phase 2" section's site map and "Shared tab toolbar" note.
5. Read REQUIREMENTS_PHASE2.md, sections 1, 2, 3, and 15 (tab list only).

Scope: ONLY the blueprint scaffolding, repository-read-only wiring, and a 9-tab shell with
placeholder content. No real statistics computation yet — that starts at M14.

Tasks:
- Add new Flask blueprint(s) (e.g. `analytics`) registered into the existing app factory alongside
  Phase 1's four blueprints.
- Implement the 9-tab shell (Summary, API Statistics, End-to-End Statistics, Missing
  Correlations, Errors, Slowest Transactions, Fastest Transactions, Transaction Explorer, Export)
  per UI_DESIGN.md's Phase 2 site map — each tab can render a placeholder for now.
- Add a test that explicitly proves Phase 2 code only calls LogRepository's public methods and
  does not import Phase 1's parser/timestamp/rules internals directly — this enforces "no log
  parsing, timestamp parsing, or rule qualification" at the code level, not just by convention.
- Add a smoke test per tab route (200 response with placeholder content).
- Run the FULL test suite (Phase 1 + Phase 2) and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out: mark M13 Complete, update inventory/tests/
  context note, set Current Milestone to M14.
- Report: "Milestone M13 complete" or describe what's blocking it.
```

---

## M14 — API Configuration

```
Continuing Phase 2 of the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M13 is Complete.
2. Read MILESTONES.md, Design Note 1, and section "M14 — API Configuration."
3. Read UI_DESIGN.md, "Screen 8 — API Configuration."
4. Read REQUIREMENTS_PHASE2.md, section 4.

Scope: ONLY API configuration (up to 4 APIs, each with Name + Entry/Exit/Error Indicator). Do NOT
apply these indicators against real records yet — that's M16.

Tasks:
- Implement core/api_config/: ApiConfig model, validation (max 4 APIs, indicator well-formed),
  reusing Phase 1's core/rules Condition/Operator classes for each Indicator rather than building
  a parallel matcher (per Design Note 1 — if you find yourself writing a second field/operator/
  value matcher, stop and reuse the existing one instead).
- Implement the API Configuration screen per UI_DESIGN.md Screen 8, including JSON save/load of
  named presets (mirror Phase 1's FieldMap preset pattern from M1).
- Write unit tests: valid config, a 5th API rejected, malformed indicator rejected with a clear
  error, preset save/load round-trip.
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M15.
- Report: "Milestone M14 complete" or describe what's blocking it.
```

---

## M15 — Transaction Builder

```
Continuing Phase 2 of the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M13 is Complete (M15 only needs the repository, not
   M14's API config).
2. Read MILESTONES.md, section "M15 — Transaction Builder."
3. Read REQUIREMENTS_PHASE2.md, section 5.

Scope: ONLY grouping LogRepository records by Correlation ID and ordering each group
chronologically. Do NOT classify events as entry/exit/error yet — that's M16.

Tasks:
- Implement core/transactions/builder.py: build_transactions(repository) -> dict[correlation_id,
  list[LogRecord]], ordered by the Phase 1 normalized timestamp (never the raw preserved string).
- Decide and document a tie-break rule for same-timestamp events (e.g. stable by internal_id) and
  test it explicitly.
- Write unit tests: grouping correctness, chronological ordering correctness including the
  tie-break case, single-record and empty correlation groups handled without error.
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M16.
- Report: "Milestone M15 complete" or describe what's blocking it.
```

---

## M16 — API Entry/Exit/Error Matching

```
Continuing Phase 2 of the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M14 and M15 are Complete.
2. Read MILESTONES.md, section "M16 — API Entry/Exit/Error Matching."
3. Read REQUIREMENTS_PHASE2.md, section 6.

Scope: ONLY matching each configured API's indicators against each transaction's ordered events,
and validating the result. Do NOT compute aggregate statistics yet — that's M17.

Tasks:
- Implement core/transactions/matching.py applying an API's indicators (M14) to a transaction's
  ordered events (M15); produce a documented status enum (e.g. Success / Failed / Error /
  Incomplete) plus Entry/Exit timestamps and elapsed time.
- Implement the validations exactly as listed in section 6: single entry, single exit-or-error,
  exit after entry.
- Design a shared anomaly vocabulary/classification for violations (missing entry, missing exit,
  duplicate entry, duplicate exit, exit-before-entry, etc.) — write it so M20 can reuse it
  directly without re-deriving the logic. Document the vocabulary in PROJECT_STATUS.md's
  Architecture Decisions Log since it isn't yet a formal ADR.
- Write unit tests covering every case: clean single entry/exit, missing entry, missing exit,
  duplicate entry, duplicate exit, error-only, exit-before-entry (must be flagged, never silently
  accepted).
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M17. Make sure
  the anomaly vocabulary is clearly documented in the Context note since M20 depends on it
  directly.
- Report: "Milestone M16 complete" or describe what's blocking it.
```

---

## M17 — API Statistics Engine

```
Continuing Phase 2 of the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M16 is Complete.
2. Read MILESTONES.md, Design Note 2, and section "M17 — API Statistics Engine."
3. Read UI_DESIGN.md, "Screen 10 — API Statistics."
4. Read REQUIREMENTS_PHASE2.md, section 7.

Scope: ONLY per-API aggregate statistics from M16's matched results. Do NOT compute cross-API
end-to-end statistics yet — that's M18. UI can be minimal; M24 polishes sort/paginate/search/
export across all tabs.

Tasks:
- Implement a shared core/stats/ percentile/stddev utility (per Design Note 2) — explicitly
  choose and document the percentile method (e.g. nearest-rank or linear interpolation), and test
  it against a small hand-computed dataset so the choice is verifiable, not implicit.
- Implement core/stats/api_stats.py computing the full section-7 list per configured API:
  transaction/entry/exit/error counts, successful/failed counts, missing/duplicate entry/exit
  counts, TPS (incoming/outgoing/peak/average, per-second and per-minute), response time
  min/max/avg/median/P90/P95/P99/stddev.
- Explicitly document and test the TPS bucketing rule (how "per second"/"per minute" windows are
  formed) and how Peak differs from Average.
- Implement the API Statistics screen per UI_DESIGN.md Screen 10 (API selector dropdown).
- Write unit tests: each statistic individually against a hand-computed fixture.
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M18.
- Report: "Milestone M17 complete" or describe what's blocking it.
```

---

## M18 — End-to-End Statistics

```
Continuing Phase 2 of the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M16 and M17 are Complete.
2. Read MILESTONES.md, section "M18 — End-to-End Statistics."
3. Read UI_DESIGN.md, "Screen 11 — End-to-End Statistics."
4. Read REQUIREMENTS_PHASE2.md, section 8.

Scope: ONLY end-to-end (cross-API) statistics per completed transaction, reusing M17's shared
percentile utility — do not write a second percentile implementation.

Tasks:
- Define and document a precise, testable definition of "completed transaction" (section 8
  assumes this without defining it — e.g. at least one matched entry and one matched exit across
  the configured APIs).
- Implement core/stats/e2e_stats.py: per-transaction Start (first API entry) / End (last API
  exit) / elapsed, plus min/max/avg/median/P90/P95/P99/stddev across all completed transactions,
  and a success/failure summary.
- Implement the End-to-End Statistics screen per UI_DESIGN.md Screen 11.
- Write unit tests against a fixture mixing complete and incomplete transactions, confirming
  incomplete ones are excluded from end-to-end stats but still accounted for somewhere (you'll
  cross-check this against M20 later — don't let a transaction silently vanish from both).
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M19.
- Report: "Milestone M18 complete" or describe what's blocking it.
```

---

## M19 — Error Statistics

```
Continuing Phase 2 of the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M16 is Complete.
2. Read MILESTONES.md, section "M19 — Error Statistics."
3. Read UI_DESIGN.md, "Screen 12 — Errors."
4. Read REQUIREMENTS_PHASE2.md, section 9.

Scope: ONLY error aggregation, consuming M16's error-classified records directly — do not
re-derive error detection logic.

Tasks:
- Implement core/stats/error_stats.py: total errors, errors per API, error percentage, top error
  messages (with a documented tie-break for ranking), error distribution by API.
- Implement the Errors tab per UI_DESIGN.md Screen 12 (Correlation ID, API, Timestamp, Error
  Indicator, Error Message columns) — basic sort/paginate/search is fine for now, M24 polishes it.
- Write unit tests: error counts/percentages, top-error-messages ranking, per-API distribution.
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M20.
- Report: "Milestone M19 complete" or describe what's blocking it.
```

---

## M20 — Missing Correlation Analysis

```
Continuing Phase 2 of the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M16 and M18 are Complete.
2. Read MILESTONES.md, section "M20 — Missing Correlation Analysis."
3. Read UI_DESIGN.md, "Screen 13 — Missing Correlations."
4. Read REQUIREMENTS_PHASE2.md, section 10.

Scope: ONLY surfacing anomalies M16 already classified, as a report. Do NOT write any new
anomaly-detection logic here — reuse M16's shared anomaly vocabulary directly.

Tasks:
- Implement core/stats/missing_correlation.py reporting every anomaly type from section 10:
  missing entry, missing exit, missing intermediate API, duplicate entry, duplicate exit,
  incomplete transaction.
- Implement the Missing Correlations tab per UI_DESIGN.md Screen 13 (Correlation ID, API, Missing
  Component, Remarks columns).
- Write unit tests: every anomaly type represented in a fixture and correctly reported. Cross-
  check against M18's "completed transaction" accounting to confirm no transaction silently
  disappears from both reports.
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M21.
- Report: "Milestone M20 complete" or describe what's blocking it.
```

---

## M21 — Slowest & Fastest Transactions

```
Continuing Phase 2 of the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M18 is Complete.
2. Read MILESTONES.md, Design Note 3, and section "M21 — Slowest & Fastest Transactions."
3. Read UI_DESIGN.md, "Screens 14 & 15 — Slowest / Fastest Transactions."
4. Read REQUIREMENTS_PHASE2.md, sections 11 and 12.

Scope: ONLY the Top-N slowest/fastest transaction lists, backed by one shared ranking utility
(not two separate implementations).

Tasks:
- Implement one shared ranking function taking M18's per-transaction elapsed times and a
  configurable N (default 20); Fastest = ascending, Slowest = descending.
- Implement both tabs per UI_DESIGN.md Screens 14/15 (Rank, Correlation ID, API, Entry Time, Exit
  Time, Elapsed Time columns).
- Write unit tests: Top-N correctness, N larger than available transactions handled gracefully, a
  documented tie-break rule when elapsed times are equal.
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M22.
- Report: "Milestone M21 complete" or describe what's blocking it.
```

---

## M22 — Transaction Explorer

```
Continuing Phase 2 of the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M15 is Complete.
2. Read MILESTONES.md, section "M22 — Transaction Explorer."
3. Read UI_DESIGN.md, "Screen 16 — Transaction Explorer."
4. Read REQUIREMENTS_PHASE2.md, section 13.

Scope: ONLY search-by-Correlation-ID and timeline display, reusing M15's transaction builder
output directly — no new grouping/ordering logic.

Tasks:
- Implement the Transaction Explorer tab per UI_DESIGN.md Screen 16: search box, timeline view
  showing event sequence, entry/exit timestamps, elapsed time, transaction status, sorted
  chronologically.
- Write integration tests: a known Correlation ID returns the exact expected timeline; an unknown
  ID produces a clear "not found" state, not an error page.
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M23.
- Report: "Milestone M22 complete" or describe what's blocking it.
```

---

## M23 — Summary Dashboard

```
Continuing Phase 2 of the Kibana Log Verification Engine build.

1. Read PROJECT_STATUS.md in full — confirm M17 and M18 are Complete.
2. Read MILESTONES.md, section "M23 — Summary Dashboard."
3. Read UI_DESIGN.md, "Screen 9 — Summary Dashboard."
4. Read REQUIREMENTS_PHASE2.md, section 14.

Scope: aggregate numbers ALREADY produced by M17 (API stats) and M18 (end-to-end stats). Do not
invent new counting logic here — if a required number isn't available from M17/M18's output,
stop and report that as a blocker rather than patching around it.

Tasks:
- Implement the Summary Dashboard per UI_DESIGN.md Screen 9: the cross-API metric table
  (Entries/Exits/Errors/Incoming TPS/Outgoing TPS/Average/P95/P99) for up to 4 configured APIs,
  showing "—" for unconfigured API slots, plus the Overall Summary block.
- Write an integration test confirming summary values match M17/M18's outputs exactly, for 1, 2,
  and 4 configured APIs (boundary cases).
- Run the FULL test suite and confirm everything passes.

Before stopping:
- Update PROJECT_STATUS.md per the standard close-out, set Current Milestone to M24.
- Report: "Milestone M23 complete" or describe what's blocking it (including if you hit the
  "number not available" case above).
```

---

## M24 — Cross-Cutting UI Polish: Sorting, Pagination, Search & Export

```
Continuing Phase 2 of the Kibana Log Verification Engine build. This is the final milestone of
Phase 2 (and of the whole project as currently planned).

1. Read PROJECT_STATUS.md in full — confirm M13-M23 are all Complete.
2. Read MILESTONES.md, Design Notes 4 and 5, and section "M24 — Cross-Cutting UI Polish."
3. Read UI_DESIGN.md, "Shared tab toolbar" and "Screen 17 — Export."
4. Read REQUIREMENTS_PHASE2.md, sections 15 and 16.

Scope: make every Phase 2 table (across all 9 tabs) consistently support sorting on every column
(ascending/descending, same convention as Phase 1's M9), pagination, search, and export to CSV
and Excel. No new statistics or business logic in this milestone — purely consolidating UI
behavior that M17-M23 implemented inconsistently as stubs.

Tasks:
- Build one shared Jinja2 table-rendering macro implementing sort/paginate/search/export, and
  retrofit every Phase 2 tab (Summary, API Statistics, End-to-End Statistics, Missing
  Correlations, Errors, Slowest Transactions, Fastest Transactions, Transaction Explorer) to use
  it instead of any ad hoc per-tab implementation built earlier.
- Implement Export: CSV via stdlib csv, Excel via openpyxl (add openpyxl to requirements.txt).
  Export must reflect the current filter/sort/search state of the tab being exported, not the
  unfiltered full dataset.
- Write integration tests on at least 3 representative tabs (e.g. API Statistics, Slowest
  Transactions, Error Statistics): sort (every column, both directions), paginate, search, and
  export all work, and exported file content matches what's on screen.
- Run the FULL test suite — all 25 milestones' tests together — and confirm everything is green.

Before stopping:
- Update PROJECT_STATUS.md: mark M24 Complete, set Overall Progress to 25/25, and write a final
  "Context for Next Agent Session" note summarizing the complete project state.
- Report: "Phase 2 complete — all 25 milestones done" or describe what's blocking final closeout.
```
