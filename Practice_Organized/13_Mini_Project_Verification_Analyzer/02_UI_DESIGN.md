# UI Design — Kibana Log Verification Engine (Phase 1)

Stack per `ARCHITECTURE.md`: Jinja2 + Bootstrap 5 + htmx, server-rendered, no SPA.
Each screen below is tagged with the milestone (from `MILESTONES.md`) that builds it.

---

# UI Design — Kibana Log Verification Engine (Phase 1 + Phase 2)

Stack per `ARCHITECTURE.md`: Jinja2 + Bootstrap 5 + htmx, server-rendered, no SPA. This applies to
Phase 2 as well — no new frontend stack is introduced for the Phase 2 tabs.
Each screen below is tagged with the milestone (from `MILESTONES.md`) that builds it.

---

## Site map

```
PHASE 1
┌─ Step 1: Load Log File ───────────[M2]
├─ Step 2: Field Mapping ───────────[M1]
├─ Step 3: Timestamp & Correlation ─[M3,M4]
│        (wizard ends here — repository is now populated)
│
├─ Rule Manager ─────────────────────[M6]
│     └─ Rule Results ────────────────[M7,M8]
├─ Log Viewer ───────────────────────[M9]
│     └─ Search & Filter panel ───────[M10]
└─ Verification Summary ─────────────[M11]

PHASE 2 (separate top-level nav item, e.g. "Analytics" — see below)
├─ API Configuration ─────────────────[M14]
└─ Analytics tabs ────────────────────[M13]
      ├─ Summary ──────────────────────[M23]
      ├─ API Statistics ───────────────[M17]
      ├─ End-to-End Statistics ────────[M18]
      ├─ Missing Correlations ─────────[M20]
      ├─ Errors ───────────────────────[M19]
      ├─ Slowest Transactions ─────────[M21]
      ├─ Fastest Transactions ─────────[M21]
      ├─ Transaction Explorer ─────────[M22]
      └─ Export ───────────────────────[M24]
```

Top nav (Phase 1, persistent once data is loaded): **Load New File | Field Mapping | Rules | Log
Viewer | Summary**. Before a file is loaded, only "Load New File" is reachable — the rest redirect
back to Step 1 with a flash message.

Top nav gains one more item once Phase 2 exists: **Analytics**, which is itself disabled (tooltip
"Configure APIs first") until at least one API is configured (M14). Inside Analytics, the 9
sub-tabs from P2 §15 sit as a secondary tab bar (see "Phase 2" section below for the wireframe).

---

## Screen 1 — Load Log File [M2]

```
┌────────────────────────────────────────────────────────────┐
│  Step 1 of 3 — Load Log File                                │
├────────────────────────────────────────────────────────────┤
│  ○ Upload CSV file        ○ Local file path                 │
│                                                               │
│  [ Choose File... ]   or   [ /var/logs/kibana_export.csv  ] │
│                                                               │
│  Delimiter: [ , ▾ ]   Encoding: UTF-8 (fixed)                │
│                                                               │
│                                   [ Load File → ]            │
├────────────────────────────────────────────────────────────┤
│  Results                                                     │
│  Total Records:     128,403                                  │
│  Loaded Records:    127,991                                  │
│  Skipped Records:   412        [ View skipped report ]       │
│  Parsing Errors:    0          [ View error report ]         │
└────────────────────────────────────────────────────────────┘
```
Notes: delimiter dropdown (comma/semicolon/tab/pipe + custom). Result counts populate after load
completes (htmx swap, since large files may take a moment — show a simple progress/spinner state).
"View skipped report" opens a small table of the first N skipped rows + reason (blank / malformed).

---

## Screen 2 — Field Mapping [M1]

```
┌────────────────────────────────────────────────────────────┐
│  Step 2 of 3 — Field Mapping                                │
├────────────────────────────────────────────────────────────┤
│  Detected columns from file: Timestamp, corr_id, app, ...   │
│                                                               │
│  Canonical Field     Source Column                          │
│  Timestamp           [ Timestamp        ▾ ]                 │
│  CorrelationId       [ corr_id          ▾ ]                 │
│  Application         [ app              ▾ ]                 │
│  API                 [ api_name         ▾ ]                 │
│  Logger               [ logger           ▾ ]                 │
│  Thread               [ thread_name      ▾ ]                 │
│  Message             [ msg              ▾ ]                 │
│  Payload             [ payload          ▾ ]                 │
│  Elapsed             [ elapsed_ms       ▾ ]                 │
│  LogLevel            [ level            ▾ ]                 │
│  TracePoint          [ trace_point      ▾ ]                 │
│                                                               │
│  Mapping preset: [ Save as... ]  [ Load preset ▾ ]           │
│                                          [ Continue → ]      │
└────────────────────────────────────────────────────────────┘
```
Notes: dropdowns are populated from the actual file headers detected in Screen 1 (column list
comes back with the load result) — never hardcoded. Presets let a recurring Kibana export shape
be reused without re-mapping every time.

---

## Screen 3 — Timestamp & Correlation Configuration [M3, M4]

```
┌────────────────────────────────────────────────────────────┐
│  Step 3 of 3 — Timestamp & Correlation                      │
├────────────────────────────────────────────────────────────┤
│  Timestamp Format                                            │
│  ○ yyyy-MM-dd HH:mm:ss.SSS                                   │
│  ○ yyyy/MM/dd HH:mm:ss.SSS                                   │
│  ○ yyyy-MM-dd'T'HH:mm:ss.SSS'Z'                              │
│  ○ ISO-8601                                                  │
│                                                               │
│  Correlation ID Pattern:  [ SFDC*                  ]        │
│                                                               │
│                                       [ Apply → ]            │
├────────────────────────────────────────────────────────────┤
│  Results                                                      │
│  Total Matching Records:  98,210                              │
│  Ignored Records:         29,781                               │
│  Invalid Timestamps:      0          [ View details ]        │
└────────────────────────────────────────────────────────────┘
```
On "Apply," the repository (M5) is populated: timestamps parsed/normalized (original preserved),
correlation pattern applied, eligible records stored with internal IDs. This is the last step of
the wizard — top nav unlocks after this.

---

## Screen 4 — Rule Manager [M6]

```
┌────────────────────────────────────────────────────────────┐
│  Rules                                    [ + New Rule ]    │
│                                            [ Import (JSON/Text) ] │
├────────────────────────────────────────────────────────────┤
│  Enabled  Name        Priority  Severity   Actions          │
│  ☑        Rule-1      1         High       [Edit][Dup][Del] │
│  ☑        Rule-2      2         Medium     [Edit][Dup][Del] │
│  ☐        Rule-3      3         Low        [Edit][Dup][Del] │
└────────────────────────────────────────────────────────────┘
```

**New / Edit Rule form:**
```
Rule Name:        [ Rule-1                    ]
Description:      [ Entry log with partition  ]
Enabled:           ☑      Priority: [1▾]   Severity: [High▾]
Expected Occurrence: [ Any ▾ ]   (Any / Exactly N / At least N)

Conditions (up to 5)                       Logical Op between conditions
1) Field [LogLevel ▾]  Op [Equals ▾]    Value [ENTRY        ]
                                            [ AND ▾ ]
2) Field [Message  ▾]  Op [Contains▾]   Value [Partition    ]
[ + Add condition ]

                                    [ Save Rule ]
```
Field dropdown is populated from the active Field Mapping's canonical names (never hardcoded —
"Any mapped field" per spec). Operator dropdown shows the 10 supported operators.

---

## Screen 5 — Rule Results [M7, M8]

```
┌────────────────────────────────────────────────────────────┐
│  [ ▶ Run All Rules ]                                         │
├────────────────────────────────────────────────────────────┤
│  Rule Name   Matches   Exec Time   Severity   Actions       │
│  Rule-1      4,210     12ms        High       [View]        │
│  Rule-2      891       9ms         Medium     [View]        │
│  Rule-3      0         3ms         Low        [View]        │
└────────────────────────────────────────────────────────────┘
```

**Rule Result detail (click "View"):**
```
┌────────────────────────────────────────────────────────────┐
│  Rule-1 — Matching Records (4,210)            [ ← Back ]    │
├────────────────────────────────────────────────────────────┤
│ ID │ Timestamp        │ CorrId    │ App  │ API │ Message │...│
│ 1  │ 2026-06-18 10:00 │ SFDC-001  │ ord  │ /v1 │ Entry...│   │
│ ...                                              [Expand row]│
└────────────────────────────────────────────────────────────┘
```
Columns exactly per Section 9: Internal Log ID, Timestamp, Correlation ID, Application, API,
Message, Payload, Elapsed, Log Level, plus an expandable "Complete Log" per row. Paginated via
htmx (large match sets shouldn't render all at once).

---

## Screen 6 — Log Viewer [M9, M10]

```
┌────────────────────────────────────────────────────────────┐
│ ○ Show All   ○ Filter by Rule [Rule-1 ▾]   🔍 [ search... ] │
│ Columns: [ ☑Timestamp ☑CorrId ☑Message ☐Payload ☑Elapsed ]  │
├────────────────────────────────────────────────────────────┤
│ ID ↕│ Timestamp ↕   │ CorrId │ Message            │ Elapsed │
│ 1   │ 2026-06-18... │ SFDC-1 │ Entry: Partition... │ 120ms   │
│ ...                                                          │
├────────────────────────────────────────────────────────────┤
│        ◀ Prev   Page 3 of 412   Next ▶      Rows/page: [50▾]│
└────────────────────────────────────────────────────────────┘
```
Column checkboxes persist for the session (ADR-9). Sort by clicking a column header (↕). Search
box does a free-text match across visible columns via htmx partial swap of just the table body.

---

## Search & Filter panel [M10]

Opens as a collapsible sidebar or modal from the Log Viewer toolbar:
```
┌─ Filters ──────────────────┐
│ Correlation ID: [ SFDC* ]  │
│ API:            [        ] │
│ Application:    [        ] │
│ Logger:         [        ] │
│ Thread:         [        ] │
│ Message:        [        ] │
│ Payload:        [        ] │
│ Elapsed:        [ > ][5000]│
│ Log Level:      [ENTRY,EXIT▾ (multi)]│
│ Timestamp:      [from] [to]│
│ Rule Name:      [Rule-1 ▾] │
│         [ Apply ] [ Clear ]│
└─────────────────────────────┘
```

---

## Screen 7 — Verification Summary [M11]

```
┌────────────────────────────────────────────────────────────┐
│  Verification Summary                                        │
├────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │  Total   │ │ Eligible │ │ Ignored  │ │ Invalid  │        │
│  │ 128,403  │ │  98,210  │ │  29,781  │ │    0     │        │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ Loaded   │ │ Rules Run│ │  Matches │ │ Failures │        │
│  │  98,210  │ │     5    │ │   5,101  │ │    0     │        │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│  Processing Time: 1.8s                                       │
└────────────────────────────────────────────────────────────┘
```
Deliberately just stat cards — no charts/metrics, per Section 12 and the explicit "no TPS/P95/P99
in this phase" boundary.

---

## Cross-cutting UI notes

- **Flash messages** (Bootstrap alerts) for every error path: invalid timestamp format, no file
  loaded yet, rule save validation errors, etc.
- **Wizard guard**: Rules/Viewer/Summary nav items are disabled (greyed, tooltip "Load a file
  first") until Step 3 of the load wizard completes.
- **Large-file feedback**: load/apply actions on big files show a spinner state, not a frozen
  page — backed by the chunked loader (ADR-5), result panel fills in via htmx once the report is
  ready.
- **No client-side framework** — every interactive bit above is implemented as a Flask route
  returning either a full page or an htmx partial; there is no separate frontend build step at
  any milestone.

---

# Phase 2 — Distributed Transaction Statistics & Performance Analyzer

Reached via the **Analytics** top-nav item (disabled until at least one API is configured).
All tabs below share one tab bar; switching tabs is an htmx partial swap of the content area only
(tab bar itself doesn't re-render). Every table on every tab below supports sort (every column,
ascending/descending — M24), pagination, search, and export (CSV/Excel — M24); individual
wireframes don't repeat that toolbar each time, see "Shared tab toolbar" at the end.

## Screen 8 — API Configuration [M14]

```
┌────────────────────────────────────────────────────────────┐
│  API Configuration                          [ + Add API ]  │
│  (up to 4)                                                   │
├────────────────────────────────────────────────────────────┤
│  API 1: [ Customer API            ]                  [ X ]  │
│    Entry Indicator:  Field[Message▾] Op[Contains▾] Val[Customer Request ] │
│    Exit Indicator:   Field[Message▾] Op[Contains▾] Val[Customer Response] │
│    Error Indicator:  Field[Message▾] Op[Contains▾] Val[Customer Error   ] │
│  ──────────────────────────────────────────────────────────  │
│  API 2: [ Order API               ]                  [ X ]  │
│    ...                                                        │
│                                          [ Save Configuration ]│
└────────────────────────────────────────────────────────────┘
```
Field dropdown sourced from the active Phase 1 FieldMap's canonical names — same convention as
Phase 1's Rule Manager (M6), since an Indicator is just a Condition (Design Note 1 in
`MILESTONES.md`). "+ Add API" is disabled past 4. Save unlocks the Analytics nav item.

## Screen 9 — Summary Dashboard [M23]

```
┌────────────────────────────────────────────────────────────┐
│ Summary                                                       │
├────────────────────────────────────────────────────────────┤
│ Metric          │ Customer API │ Order API │ API3 │ API4    │
│ Entries         │   12,400     │  12,398   │  —   │  —      │
│ Exits           │   12,395     │  12,390   │  —   │  —      │
│ Errors          │       5      │      8    │  —   │  —      │
│ Incoming TPS    │     34.2     │    34.1   │  —   │  —      │
│ Outgoing TPS    │     34.0     │    33.9   │  —   │  —      │
│ Average (ms)    │     120      │     340   │  —   │  —      │
│ P95 (ms)        │     410      │     980   │  —   │  —      │
│ P99 (ms)        │     800      │    1500   │  —   │  —      │
├────────────────────────────────────────────────────────────┤
│ Overall Summary                                                │
│ Total Transactions: 12,400   Success Rate: 99.6%               │
│ Avg End-to-End: 460ms   P95: 1,400ms   P99: 2,100ms             │
│ Failure Rate: 0.4%                                              │
└────────────────────────────────────────────────────────────┘
```
Columns for unconfigured APIs (3/4 if fewer than 4 are set up) show "—", not blank/error. Every
number here is pulled from M17/M18's already-computed output, never recalculated locally.

## Screen 10 — API Statistics [M17]

```
┌────────────────────────────────────────────────────────────┐
│ API Statistics              API: [ Customer API ▾ ]          │
├────────────────────────────────────────────────────────────┤
│ Transaction Counts: 12,400   Successful: 12,390  Failed: 10  │
│ Entry: 12,400  Exit: 12,395  Error: 5                         │
│ Missing Entry: 0  Missing Exit: 5  Dup Entry: 0  Dup Exit: 0  │
├────────────────────────────────────────────────────────────┤
│ TPS                  Per Second   Per Minute                  │
│ Incoming             34.2         2,052                       │
│ Outgoing             34.0         2,040                        │
│ Peak Incoming        58.0         3,100                        │
│ Peak Outgoing        57.5         3,050                        │
│ Average              34.1         2,046                        │
├────────────────────────────────────────────────────────────┤
│ Response Time (ms)   Min  Max   Avg  Median  P90  P95  P99  StdDev │
│                       12  4200   120    98    310  410  800   95   │
└────────────────────────────────────────────────────────────┘
```
API selector dropdown switches which configured API's stats are shown (htmx partial swap).

## Screen 11 — End-to-End Statistics [M18]

```
┌────────────────────────────────────────────────────────────┐
│ End-to-End Statistics                                          │
├────────────────────────────────────────────────────────────┤
│ Total Transactions: 12,400   Successful: 12,350  Failed: 50   │
│ Success %: 99.6%   Failure %: 0.4%                              │
├────────────────────────────────────────────────────────────┤
│ End-to-End Time (ms)  Min  Max   Avg  Median  P90  P95  P99  StdDev │
│                        45  9800   460   380    900 1400 2100  310   │
└────────────────────────────────────────────────────────────┘
```

## Screen 12 — Errors [M19]

```
┌────────────────────────────────────────────────────────────┐
│ Errors                                                         │
├────────────────────────────────────────────────────────────┤
│ Total Errors: 13   Error %: 0.1%                                │
│ Top Error Messages: "Timeout" (8), "Invalid Payload" (5)         │
├────────────────────────────────────────────────────────────┤
│ CorrId    │ API          │ Timestamp        │ Indicator │ Message │
│ SFDC-441  │ Customer API │ 2026-06-18 10:02 │ Error     │ Timeout │
│ ...                                                              │
└────────────────────────────────────────────────────────────┘
```

## Screen 13 — Missing Correlations [M20]

```
┌────────────────────────────────────────────────────────────┐
│ Missing Correlations                                            │
├────────────────────────────────────────────────────────────┤
│ CorrId    │ API          │ Missing Component  │ Remarks         │
│ SFDC-552  │ Order API    │ Exit               │ No exit found   │
│ SFDC-560  │ Customer API │ Intermediate (Kafka)│ Sequence gap   │
│ ...                                                              │
└────────────────────────────────────────────────────────────┘
```

## Screens 14 & 15 — Slowest / Fastest Transactions [M21]

Identical layout, opposite sort order, separate tabs:
```
┌────────────────────────────────────────────────────────────┐
│ Slowest Transactions          Top N: [ 20 ▾ ]                 │
├────────────────────────────────────────────────────────────┤
│ Rank │ CorrId    │ API          │ Entry Time │ Exit Time │ Elapsed │
│  1   │ SFDC-901  │ Order API    │ 10:00:01   │ 10:00:11  │ 9800ms  │
│ ...                                                              │
└────────────────────────────────────────────────────────────┘
```
"Fastest Transactions" tab is the same table sorted ascending by Elapsed instead of descending.

## Screen 16 — Transaction Explorer [M22]

```
┌────────────────────────────────────────────────────────────┐
│ Transaction Explorer     🔍 Correlation ID: [ SFDC-441    ] │
├────────────────────────────────────────────────────────────┤
│ Status: Failed (Error in Customer API)                         │
│                                                                   │
│ Timeline (chronological)                                         │
│ 10:00:01.120  Customer API   Entry                                │
│ 10:00:01.890  Customer API   Error  ("Timeout")                   │
│                                                                   │
│ API Sequence: Customer API (Entry → Error)                        │
└────────────────────────────────────────────────────────────┘
```
Unknown Correlation ID → "No transaction found for SFDC-XXX" message, not an error page.

## Screen 17 — Export [M24]

```
┌────────────────────────────────────────────────────────────┐
│ Export                                                          │
├────────────────────────────────────────────────────────────┤
│ Export which tab's current (filtered/sorted) view?               │
│ [ Summary ▾ ]                                                    │
│ Format:  ○ CSV   ○ Excel                                          │
│                                          [ Download ]            │
└────────────────────────────────────────────────────────────┘
```
Export always reflects the current filter/sort/search state of the selected tab, not the
unfiltered full dataset — what's on screen is what's exported.

## Shared tab toolbar [M24]

Every Phase 2 tab (Screens 9–16) renders this same toolbar above its table, via one shared Jinja2
macro (per `MILESTONES.md` Design Note 4):
```
🔍 [ search...]      Columns sortable via header click (↑/↓)      [Export ▾]
                                              ◀ Prev  Page X of Y  Next ▶
```
