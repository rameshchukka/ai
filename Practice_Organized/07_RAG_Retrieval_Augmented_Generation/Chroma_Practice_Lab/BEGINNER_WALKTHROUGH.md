# Beginner Walkthrough — Chroma Practice Lab + Navigator

One linear path, in the order to actually run things. Skip nothing on your
first pass — each step assumes the previous one worked.

## Before Step 1 — one-time setup

**1. Put your `inhouse_llm.py` in 3 places.** Copy your real, working
`inhouse_llm.py` file (the one with your rotated/working API key) into all
three of these folders:
```
chroma_practice_lab/inhouse_llm.py
chroma_practice_lab/ingestion/inhouse_llm.py
chroma_navigator/inhouse_llm.py
```
(The corrected `inhouse_wrappers.py` is already sitting in those same 3
folders — I put it there for you. You only need to add `inhouse_llm.py`
yourself, since it has your org's real credentials and I won't generate or
copy that file's contents myself.)

**2. Install everything you need, once:**
```bash
pip install chromadb pandas openpyxl numpy scikit-learn matplotlib requests streamlit plotly langchain-openai langchain-core --break-system-packages
```

**3. Open two terminal windows.** You'll keep one running the Chroma server
the whole time, and use the other for everything else. (On Mac: Terminal app,
Cmd+T for a new tab. On Windows: PowerShell, open two separate windows.)

---

## Step 1 — Build embedding-space intuition (no server needed yet)

**File:** `chroma_practice_lab/ConceptualIntuition.ipynb`

**How to open it:** in Terminal 2, `cd` into `chroma_practice_lab`, then run:
```bash
jupyter notebook
```
This opens a browser tab showing your files. Click `ConceptualIntuition.ipynb`.

**What to do:** click the first code cell, then press `Shift+Enter` repeatedly
to run each cell top to bottom, one at a time. Don't run them all at once on
your first pass — read each output before moving on.

**What you should observe, cell by cell:**
- Setup cell: prints `(55, 5) (55, 1024)` or similar — confirms 55 rows loaded
  and each got a 1024-number vector.
- Section 2 (near-duplicates): three lines like `dup_01 vs ... similarity = 0.95+`
  — a HIGH number close to 1.0. This is the "paraphrase landed near its
  original" check.
- Section 3 (bridge docs): two similarity numbers per bridge doc, both
  noticeably higher than the "other clusters" number.
- Section 5: a plot window/image appears — two scatter plots, dots grouped
  into visible clumps by color.
- Section 6 (recall@k): a list of topics each with a score near `1.00`.

**If something looks wrong:** a recall score way below 1.0, or dots in
section 5 NOT forming visible groups, means something's off with the
embedding call itself — stop here and fix it before moving to Step 2,
since every later step depends on embeddings working correctly.

---

## Step 2 — Start the Chroma server

**Terminal 1** (the one you're leaving open):
```bash
pip install chromadb --break-system-packages
chroma run --path ./chroma_data --port 8000
```
Run this from wherever you want the database files to live — `chroma_data`
will be created automatically.

**What you should observe:** the terminal prints something like
`Uvicorn running on http://0.0.0.0:8000` and then just sits there, not
returning to a prompt. **That's correct — leave this terminal open and
untouched for the rest of the walkthrough.** If it exits immediately back to
a prompt, something failed — read the error text above the prompt.

---

## Step 3 — Load the practice data into Chroma

**File:** `chroma_practice_lab/ingestion/bulk_ingest_from_excel.ipynb`

**Terminal 2:** `cd` into `chroma_practice_lab/ingestion`, run `jupyter notebook`,
open this file.

**Run cells top to bottom, one at a time, `Shift+Enter`.**

**What you should observe:**
- Setup cell: `Setup OK` or no error.
- "create status" cell: a number like `200` or `409` (409 just means the
  collection already existed from a previous run — also fine).
- "Collection UUID" cell: prints a long string like
  `a1b2c3d4-e5f6-...` — **this confirms Step 2's server is reachable.**
- Embedding cell: prints `Embedded rows 0 to 20`, `Embedded rows 20 to 40`,
  etc., then `Total embeddings: 55 | dim: 1024`.
- Add cell: `Added rows 0 to 20`, etc.
- Count cell: `Chroma collection count: 55` and `Expected (rows in Excel): 55`
  — **these two numbers must match.**
- Sanity query cell: for each of the 3 sample questions, the printed top
  result text should obviously relate to that question's topic (cooking
  question → cooking-related text, etc).

**If the UUID cell errors with a connection error:** Step 2's server isn't
running or isn't on port 8000 — go back and check Terminal 1.

**If counts don't match (55 vs something else):** re-run the notebook from
the top — it's most likely a partial run from before.

---

## Step 4 — Visually explore what you just loaded

**File:** `chroma_navigator/app.py`

**Terminal 2** (Jupyter can stay open in the browser; use this terminal for
a new command): `cd` into `chroma_navigator`, then:
```bash
streamlit run app.py
```

**What you should observe:** terminal prints a local URL
(`http://localhost:8501`), and it should auto-open in your browser. If not,
copy that URL into your browser manually.

**In the browser, do this exact sequence:**
1. Sidebar → **Connect via** → select **HTTP server**.
2. Host: `localhost`, Port: `8000` (matches Step 2's server).
3. Click **Connect**.
4. In the **Collection** dropdown, select `practice_dataset`.
5. Sidebar should show **Items in collection: 55** — if it shows `0` or
   errors, Step 3 didn't actually save into this same server/collection.

**Now go through each tab:**
- **📄 Browse** — you should see a table, 55 rows, with `id`/`document` columns.
  Type `vegetables` into the filter box — exactly 2 rows should appear.
- **🔎 Search** — type `How does high heat affect vegetables?` — top 2 results
  should both be the cooking/near-duplicate pair, with very close distance
  numbers to each other.
- **🗺️ Visualize** — switch **Color by** to `type`. You should see one big
  gray blob-cluster of dots, with a couple of red dots sitting right on top
  of gray ones (near-duplicates), blue dots sitting between two gray clumps
  (bridge docs), and black dots off on their own (outliers).
- **🧩 Cluster drill-down** — set k to `8`, look at the resulting colored
  groups, then pick one cluster from the dropdown and read what's actually
  inside it.

**This tab-by-tab behavior is described in more detail, with exact
expectations per row of the dataset, in `chroma_practice_lab/ChromaNavigatorGuide.md`
— read that next if you want the deeper version of "what should I be seeing."**

---

## Step 5 (optional, do this after Steps 1-4 all work) — Raw HTTP, by hand

**File:** `chroma_practice_lab/ingestion/manual_curl_examples.sh`

This is **not a script to run all at once.** Open it in a text editor, and
copy ONE command block at a time into Terminal 2, reading the actual output
before copying the next block. You'll need to paste your real `API_KEY` value
into the `API_KEY=` line near the top first.

**What you're confirming, block by block:** the literal JSON Chroma and the
Jina embedding endpoint send back and forth — this is "looking under the
hood" of what Steps 3 and 4 were doing for you automatically.

---

## Step 6 (optional, advanced) — Load testing with JMeter

Only do this once Steps 1-5 all work without errors. See
`chroma_practice_lab/IngestionProcess.md`'s JMeter section for setup —
this measures performance under load, not correctness, so it's the last
thing to try, not a troubleshooting tool.

---

## If you get stuck

Tell me exactly: which step number, what you ran, and paste the **exact**
error text or output you saw (not a paraphrase). "Step 3, the UUID cell, got
`ConnectionRefusedError`" is something I can act on immediately; "it didn't
work" isn't.
