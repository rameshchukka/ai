# Chroma Studio in Practice — Decision-Making Playbook

A guided, runnable notebook that teaches you to **use Chroma Studio's views to make
real decisions** about a corpus — not just look at pretty dots. Built around a
support knowledge base with six deliberately planted flaws, so every Studio view
reveals a specific, realistic problem and the fix it points to.

## Files
- `Chroma_Studio_Playbook.ipynb` — the guided notebook (runs offline out of the box)
- `dataset/support_kb.csv` — 21-doc enterprise support KB with planted flaws
- `build_dataset.py` — regenerates the dataset (already run; re-run to tweak it)

## What it teaches
Each section = **spot a problem in a Studio view → decide the fix → apply it → recheck**:

| # | Problem (planted in the data) | Studio view that reveals it | Decision it drives |
|---|---|---|---|
| 1 | Thin/orphan topic coverage | Visualize, color by category | Enrich content |
| 2 | Near-duplicate documents | Visualize (stacked points) + Search | Dedupe / merge |
| 3 | Metadata you can't trust | Visualize: KMeans vs category cross-tab | Investigate labels |
| 4 | Mislabeled metadata | Cluster drill-down | Fix metadata (no re-embed) |
| 5 | Overlong doc mixing 3 topics | Search returns a muddy chunk | Re-chunk (re-embeds) |
| 6 | Semantic collisions | Search: top-2 too close | Add a metadata field to filter on |
| 7 | Missing metadata | Browse: filter for blanks | Backfill, then review |

The payoff is the **repeatable checklist** at the end — the exact analyze→decide→act
loop you'd run on any new corpus at work, and the kind of thing interviews probe for.

## Run it
Works offline immediately (ships with a crude mock embedder):
```bash
pip install pandas numpy scikit-learn matplotlib
jupyter notebook Chroma_Studio_Playbook.ipynb   # or open in VS Code
```

### Make it real (recommended once you've read through it)
Replace the single `MOCK` cell near the top with your in-house embedder:
```python
from inhouse_wrappers import InHouseEmbeddings
embedder = InHouseEmbeddings()
```
Nothing else changes. With a real embedding model every section sharpens — the
mock is deliberately crude so it runs anywhere, and the notebook is upfront about
where that crudeness shows (mainly the mislabel-detection section, which depends on
neighborhood quality).

### Do it in the actual Chroma Studio app too
The notebook tells you, at each step, which Chroma Studio tab shows the same thing
(Browse / Add / Edit-Update / Visualize / Manage). Load `support_kb.csv` into a
Chroma collection via the Studio app's **Add** tab, then follow along in the UI —
the notebook is the "why," the app is the "where you'd click."

## Why a flawed dataset on purpose
Clean demo data teaches nothing — real corpora are messy, and expertise is *noticing*
the mess before it silently degrades your RAG system. The hidden `flaw` column lets
you check whether the Studio views (and your own eye) caught each planted problem.
Real data won't hand you that answer key; that's the whole point of learning the
diagnostic habit here first.
