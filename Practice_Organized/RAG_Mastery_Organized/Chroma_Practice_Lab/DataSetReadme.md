# Dataset README — `practice_dataset.xlsx`

## Purpose
A small, hand-designed dataset (55 rows) built specifically to make embedding-space
behavior *visible* — not real project data, but a controlled sandbox where you know
in advance what the "right" answer in the vector space should look like, so you can
tell whether your pipeline (embedding, ingestion, retrieval, visualization) is behaving
correctly before you point any of this at messy real data.

## Columns
| Column | Meaning |
|---|---|
| `id` | Unique row id, used as the Chroma document id during ingestion |
| `text` | The actual document text to embed |
| `topic` | Ground-truth topic label (used for coloring/validating, not sent to the model) |
| `type` | One of `core`, `near_duplicate`, `bridge`, `outlier` — see below |
| `notes` | What to expect to observe for that row, and why it was included |

## Composition (55 rows)
- **48 "core" documents** across **8 disjoint topic clusters** (6 each): cooking,
  sports, finance, travel, music, history, medicine, programming. Chosen specifically
  because they don't overlap conceptually — this is your "easy mode" baseline for
  confirming clean separation works at all.
- **3 "near_duplicate" documents** — paraphrases of an existing core document (one
  each from cooking, finance, programming). These should land *extremely* close to
  their original in embedding space. If they don't, something is wrong with your
  embedding pipeline (wrong model, inconsistent preprocessing, etc.) before you even
  get to clustering questions.
- **2 "bridge" documents** — each deliberately straddles two clusters (sports +
  medicine; travel + history). These simulate the messy reality of real data: not
  everything belongs cleanly to one topic. Watch where these land relative to their
  two parent clusters.
- **2 "outlier" documents** — topics (physics, geology) unrelated to any of the 8
  clusters. These should sit apart from everything else. If an outlier ends up buried
  inside a cluster, that's a red flag worth investigating (embedding model not
  discriminating well, or the "unrelated" topic isn't as unrelated as assumed).

## How to use this dataset across the practice exercises
1. **`ConceptualIntuition.ipynb`** — embeds every row directly (no Chroma needed yet)
   and checks the expected behavior numerically: do near-duplicates show the highest
   similarity? Do bridge docs show split similarity to two clusters? Do outliers show
   low similarity to everything?
2. **Manual curl + bulk ingest notebook** — load this exact file into a real Chroma
   collection via the REST API, both by hand (a few rows) and in bulk (all 55).
3. **Chroma Navigator** — once ingested, use the Visualize and Cluster drill-down tabs
   to *see* the same structure you confirmed numerically in step 1 — this is where the
   "does the picture match the math" intuition actually forms.
4. **JMeter** — once ingestion is correct, load-test the same endpoints with repeated
   requests to see how latency/throughput behaves under concurrency.

## Extending it for your real project
Once you're comfortable with this clean version, the most valuable next exercise is
deliberately making it messier: shorter/longer documents, more topic overlap, real
near-duplicates from your actual corpus, more outliers. Clean synthetic data teaches
you what "good" looks like; messy data teaches you what "needs fixing" looks like —
you'll need both instincts on a real project.
