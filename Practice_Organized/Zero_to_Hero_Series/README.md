# 🚀 Zero to Hero Series — Complete Index

Sixteen standalone, deeply-taught modules — each a complete course in itself: detailed theory,
ASCII diagrams, mental models, pro tips, common traps, hands-on exercises with solutions, and a
verified capstone project. Every notebook runs offline (mock LLMs/agents where needed) and is
100% JSON-validated and execution-tested. This is **complete, basics-to-expert coverage** — see
`/MASTER_CURRICULUM.md` for the full course map; every previously-identified gap is now closed.

**Format used throughout:** 📖 Theory (detailed) → 🧠 Mental model → 🖼️ ASCII diagram →
🔬 Worked example → ⚡ Pro tips → ⚠️ Common traps → ✏️ Your Turn → ✅ Solution, ending in a
🏆 capstone + 📌 quick-reference.

## Suggested Learning Order

| # | Folder | Topic | Prerequisite |
|---|---|---|---|
| 1 | `04_PyTorch_Zero_to_Hero` | Tensors, autograd, training loop, regression & classification | NumPy/Pandas lab |
| 2 | `TF_Keras_Zero_to_Hero` | TensorFlow/Keras: GradientTape, Sequential/Functional API, callbacks | NumPy/Pandas lab |
| 3 | `16_Classical_ML_Zero_to_Hero` | Regression, trees, ensembles, k-NN, k-Means, SVM, PCA | NumPy/Pandas lab |
| 4 | `11_Transformers_Attention_Zero_to_Hero` | Self-attention, multi-head attention, causal masking, mini-GPT | PyTorch or TF/Keras lab |
| 5 | `05_LLM_APIs_Prompting_Zero_to_Hero` | Roles, sampling, prompt patterns, structured output, memory | — |
| 6 | `06_Embeddings_Search_Zero_to_Hero` | TF-IDF, BM25, semantic search, hybrid search, evaluation | — |
| 7 | `07_RAG_Zero_to_Hero` | Full RAG pipeline: ingest→chunk→embed→retrieve→generate, guardrails | Embeddings & Search lab |
| 8 | `08_LangChain_Zero_to_Hero` | Runnables, LCEL, chains, parsers, memory, tools, agents | LLM APIs lab |
| 9 | `09_Agents_Orchestration_Zero_to_Hero` | ReAct loop, tool selection, memory, safety, multi-agent | LangChain lab |
| 10 | `12_MCP_Tooling_Zero_to_Hero` | Model Context Protocol: tools, resources, prompts, discovery | Agents lab |
| 11 | `13_A2A_Protocol_Zero_to_Hero` | Agent-to-agent: cards, discovery, task lifecycle, delegation | Agents + MCP labs |
| 12 | `10_Evaluation_Guardrails_Zero_to_Hero` | Eval sets, precision/recall/F1, LLM-as-judge, guardrails, regression tests | — |
| 17 | `21_Micrograd_Visual_Backprop` | Build a real, correct autograd engine from scratch (inspired by Karpathy's micrograd), rendering the computation graph at every step — verified to match real PyTorch's gradients exactly | NumPy lab (do before or alongside module 4) |
| 18 | `22_Transformers_Visual_Deep_Dive` | RNN vs Transformer measured side-by-side, real attention-weight heatmaps on real sentences, multi-head specialization, training (teacher forcing) vs inference (KV-caching) — verified to match real PyTorch's attention exactly | Module 11 (Transformers & Attention) + ideally module 17 (Micrograd) |
| 13 | `17_Vector_Search_at_Scale_Zero_to_Hero` | IVF, LSH, HNSW, Product Quantization — how real vector DBs search billions of vectors | Embeddings & Search lab |
| 14 | `18_Embedding_Model_Training_Zero_to_Hero` | Contrastive loss, triplet loss, in-batch negatives — how embedding models are actually trained | PyTorch lab + Embeddings & Search lab |
| 15 | `19_Advanced_RAG_Zero_to_Hero` | Query rewriting, cross-encoder re-ranking, HyDE, multi-hop retrieval, query routing | RAG lab |
| 16 | `20_MLOps_Production_Serving_Zero_to_Hero` | Serving patterns, latency budgets, caching, monitoring, drift detection, canary rollouts, cost management | Evaluation & Guardrails lab |

Modules 13-16 are advanced-track add-ons — do them after their prerequisite, in any order,
once you've completed modules 1-12. Module 16 (MLOps) is a natural capstone to the whole series.

## How to Use

1. Each folder is self-contained: `.ipynb` notebook + `README.md` + an interactive `*_Guide.html`.
2. Work top to bottom within a notebook — attempt every ✏️ exercise before revealing ✅.
3. Finish each notebook's 🏆 capstone before moving to the next module.
4. See `/MASTER_CURRICULUM.md` (repo root) for how this series fits into the full course, plus
   remaining advanced-track gaps (vector search at scale, embedding-model training, advanced
   RAG, MLOps) for future study.
