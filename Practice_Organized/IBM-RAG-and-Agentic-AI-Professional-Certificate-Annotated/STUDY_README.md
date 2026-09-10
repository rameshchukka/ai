# IBM RAG & Agentic AI Certificate — Full Study Companion

Every code cell in every lab notebook now has a concept note explaining what it does and why,
plus a "Fundamentals Required" primer at the top of each notebook listing the prerequisite
ideas you need before starting that lab.

## What's in each annotated notebook
1. **📘 Fundamentals Required** (top of the notebook) — a bullet list of the concepts that
   cell-by-cell notes assume you already know (e.g. "Pydantic BaseModel", "cosine similarity",
   "CLIP's shared text-image space") with a one-line explanation of each.
2. **📎 CONCEPT notes** — inserted before EVERY non-empty code cell, explaining what that
   specific cell does, referencing its actual variable/function names, and connecting it to
   the broader RAG/embeddings concepts where relevant.

Coverage (all code cells, no exceptions):
| Notebook | Fundamentals | Cell notes |
|---|---|---|
| M1L1 — Extract Structured JSON | 8 concepts | 14/14 cells |
| M1L2 — Process Multimodal Data | 8 concepts | 14/14 cells |
| M2L1 — Multimodal Vector Index | 6 concepts | 7/7 cells |
| M2L2 — Similarity Retrieval + Filtering | 5 concepts | 9/9 cells |
| M2L3 — Multimodal Fusion & Reranking | 5 concepts | 9/9 cells |

**53 code cells annotated across all 5 notebooks — full coverage, nothing skipped.**

## A note on the duplicate M1L2 file
`M1L2/M1L2_Process_Multimodal_Data_with_LLMs.ipynb` is an unsolved duplicate of the same
lab as `M1L2-Process-Multimodal-Data-with-LLMs-v1.ipynb` — per your instruction, it was left
untouched. Use the `-v1.ipynb` file (fully solved and now fully annotated) for this lab.

## How the notes were written
Every note is based on reading the ACTUAL code in that cell — no generic filler. Where a
cell implements a specific technique (few-shot prompting, Pydantic validation, CLIP's shared
embedding space, min-max score normalization, weighted fusion), the note names the technique
and explains why that cell needs it, often tying back to concepts from your broader RAG
course (e.g. M2L3's fusion weights are explicitly connected to the Pinecone alpha-scaling
explanation from earlier).

## Important
- These annotated notebooks are for **understanding**. For the **graded submission**, use
  the identical lab inside Coursera's own sandbox (WatsonX credentials are pre-provisioned
  there — the annotation cells don't affect grading, they're just extra markdown).
- **If library installs fail** in the Coursera lab: run the notebook's OWN `%pip install`
  cell (not your own), use `%pip` (percent, not `!pip`), restart the kernel after installing.
- Also in this repo: `STUDY_GUIDE.html` (a companion guide per lab), `APPENDIX_Practice_Roadmap.html`
  / `APPENDIX_Practice_Order.md` (how this fits your wider curriculum).
