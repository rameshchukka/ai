# RAG Course — Foundations to Advanced

One course, two parts, eleven runnable notebooks: from the fundamentals of RAG through
advanced retrieval. This merges the earlier Foundations and Advanced modules into a single
clean, ordered sequence.

```
guides/
├── FOUNDATIONS_GUIDE.html        Part 1 theory — concepts, ASCII diagrams, code, practice links
└── ADVANCED_RETRIEVAL_GUIDE.html Part 2 theory — TF-IDF, ANN/HNSW, cross-encoders, ColBERT, metrics, Chroma Studio

dataset/
├── corpus.csv                    24 docs (mini knowledge base, 2 domains)
├── queries.csv                   10 labeled queries -> relevant doc ids (ground truth)
└── build_dataset.py

part1_foundations/                run these first, in order
├── 01_llm_and_augmented_prompts.ipynb
├── 02_embeddings_and_cosine.ipynb
├── 03_retrieval_bm25_vs_semantic.ipynb
├── 04_retrieval_metrics.ipynb
├── 05_chunking.ipynb
└── 06_routing_multi_source.ipynb

part2_advanced/                   then these
├── 07_tfidf.ipynb
├── 08_ann_and_hnsw.ipynb
├── 09_cross_encoder_reranking.ipynb
├── 10_colbert_late_interaction.ipynb
└── 11_metrics_expanded.ipynb
```

## The full path (11 notebooks in one sequence)

**Part 1 — Foundations** (read `guides/FOUNDATIONS_GUIDE.html` alongside)
| # | Notebook | Concept |
|---|---|---|
| 01 | llm_and_augmented_prompts | the generation half of RAG |
| 02 | embeddings_and_cosine | text → vectors; cosine similarity |
| 03 | retrieval_bm25_vs_semantic | keyword vs meaning-based retrieval |
| 04 | retrieval_metrics | Precision@K, Recall@K, MRR |
| 05 | chunking | fixed / overlap / recursive splitting |
| 06 | routing_multi_source | send a query to the right source |

**Part 2 — Advanced** (read `guides/ADVANCED_RETRIEVAL_GUIDE.html` alongside)
| # | Notebook | Concept |
|---|---|---|
| 07 | tfidf | weight words by how distinctive they are |
| 08 | ann_and_hnsw | fast search at scale; the M/ef knobs |
| 09 | cross_encoder_reranking | retrieve-then-rerank for accuracy |
| 10 | colbert_late_interaction | token-level matching (MaxSim) |
| 11 | metrics_expanded | P@K, R@K, MRR, MAP, nDCG, F1 — worked |

## How to use
1. Read `guides/FOUNDATIONS_GUIDE.html`; run `part1_foundations/` 01→06 as you hit each **Practice →** box.
2. Read `guides/ADVANCED_RETRIEVAL_GUIDE.html`; run `part2_advanced/` 07→11.
3. Its final section shows how to load `dataset/corpus.csv` into Chroma Studio and *watch*
   the failing queries from notebook 04/11 to see why they missed.

## Setup
```
pip install numpy pandas scikit-learn        # core; TF-IDF + metrics are real
pip install rank_bm25 hnswlib sentence-transformers   # optional: real BM25 / HNSW / cross-encoder
jupyter notebook
```
All notebooks run **offline** (no API key). The two dataset-backed notebooks (03, 04) read
`../dataset/` — run them from inside `part1_foundations/` (Jupyter/VS Code do this automatically
when you open the notebook in place).

## Honesty note
TF-IDF and every metric are the real thing (sklearn + from-scratch math, values hand-verifiable).
The embedding-based labs use a simple offline vectorizer, and the ANN/cross-encoder/ColBERT labs
use small or mock stand-ins — each shows the one line to swap in the real model. The retrieval
math never changes; only the vectors get smarter. All 11 notebooks were executed before packaging.
```
