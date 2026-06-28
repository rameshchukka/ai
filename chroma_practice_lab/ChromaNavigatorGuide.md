# Chroma Navigator Guide — Analyzing `practice_dataset`

This assumes you've already ingested `practice_dataset.xlsx` into a Chroma collection
(via the manual curl walkthrough and/or the bulk ingest notebook) and have
`chroma_navigator` (the Streamlit tool from earlier) running and connected to it.

## Connect
Sidebar → **Connect via** → **HTTP server** → Host/Port matching your Chroma server →
**Connect** → select the `practice_dataset` collection from the dropdown.

## Tab 1: Browse — confirm the data landed correctly
- Check the row count matches 55.
- Filter by text for `"vegetables"` — you should see exactly 2 rows: `coo_01` and
  `dup_01`. If only one shows up, the near-duplicate didn't ingest — check the bulk
  notebook's Step 4/5 output.
- Sort/scan the `type` metadata column — confirm you can see `core`, `near_duplicate`,
  `bridge`, and `outlier` all represented.

## Tab 2: Search — test retrieval behavior directly
Try these queries and see if the result matches expectation:
| Query | Expect |
|---|---|
| "How does high heat affect vegetables?" | Top-2 should be `coo_01` and `dup_01`, very close distances to each other |
| "athlete injury recovery" | `brg_01` should appear, likely alongside `medicine` and/or `sports` core docs |
| "particle physics" | `out_01` should appear, but with a noticeably worse (larger) distance than any same-cluster query above |

If any of these don't match — that's your debugging entry point, not a tool failure to
shrug off. Check: did the embedding endpoint return the same vector dimension every
time? Is the collection's distance metric set to cosine (recommended for text)?

## Tab 3: Visualize — the main event
Switch to 3D PCA, color by the `type` metadata field. You should see:
- **A tight clump of gray (`core`) points forming 8 visually separated blobs** — this
  is your baseline confirmation that disjoint topics produce disjoint regions.
- **Red points (`near_duplicate`) sitting essentially on top of one core point each**
  — if a red point looks like it's floating in its own space instead of glued to its
  parent, something's off with embedding consistency (e.g., the live query embedding
  used a different model/version than what was stored).
- **Blue points (`bridge`) sitting in the gap BETWEEN two blobs**, not fully inside
  either one — this is the most interesting thing to look at, because it's the visual
  signature of "ambiguous content," which is the normal case in real corpora, not the
  exception.
- **Black points (`outlier`) sitting away from every blob**, ideally near the edges of
  the whole plot.

Switch to coloring by `topic` instead of `type` to confirm the 8 clusters are
internally coherent (all 6 cooking docs visually grouped, etc.) — switching the color
field is the fastest way to ask two different questions of the same plot.

## Tab 4: Cluster drill-down — does unsupervised clustering recover your design?
- Set **k = 8** (your true number of topics) and run KMeans. Compare the resulting
  cluster assignments to the `topic` color from Tab 3 — do they roughly agree?
- Click into whichever cluster contains a bridge document. Does KMeans assign it
  fully to one side (e.g., all the way into "sports"), or does the cluster boundary
  visibly cut close to it? This tells you something concrete about how forcing a hard
  cluster count handles genuinely ambiguous content — useful intuition for choosing
  `k` on real data where you don't know the "true" topic count in advance.
- Try **k = 10** and **k = 6** and watch what changes. At k=10, do the bridge/outlier
  docs sometimes get their own tiny "cluster" of size 1-2? At k=6, do two of your
  designed topics get merged into one cluster? Both are useful, concrete lessons about
  how sensitive KMeans cluster boundaries are to the chosen k — a parameter you'll have
  to make a real, justified choice about on your actual project data.

## What "done" looks like for this exercise
You should be able to predict, before clicking, roughly where each row will land and
what k=8 clustering will do with the bridge/outlier rows — and then confirm it. That
predictive intuition is the actual transferable skill; the specific numbers on this
toy dataset are not.
