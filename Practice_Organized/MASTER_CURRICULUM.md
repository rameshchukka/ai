# 🎓 Master Curriculum — Python & AI, Basics to Expert

A complete map of the field: what to learn, in what order, with the **theory**, **math**,
**algorithms**, and **dataset examples** needed at each stage. Each block lists status against
your existing archive: ✅ built & delivered · 🟡 partially covered · ⬜ not yet built.

---

## Level 0 — Programming Foundations
**Goal:** fluent Python before touching any math/ML.

| Topic | Covered by |
|---|---|
| Variables, control flow, loops | ✅ `01_Python_Basics` |
| Lists, tuples, sets, dicts | ✅ `01_Python_Basics` |
| Functions, closures, decorators | ✅ `01_Python_Basics` |
| OOP: classes, inheritance, dunder methods | ✅ `01_Python_Basics/09_OOPs` |
| Error handling, file I/O | ✅ `02_Python_Advanced_and_Exercises` |
| Iterators/generators, comprehensions | ✅ `02_Python_Advanced_and_Exercises` |
| Algorithms & data structures (stacks, trees, graphs, sorting, Big-O) | ✅ `19_Algorithms_and_Data_Structures` |

---

## Level 1 — Math Foundations
**Goal:** the four math pillars every ML/DL/AI topic below rests on.

| Topic | Theory | Status |
|---|---|---|
| **Linear algebra** | vectors, matrices, matrix multiply, rank, eigenvalues/eigenvectors, SVD | ✅ `20_Math_and_Statistics_Foundations` + NumPy Ch.11 |
| **Calculus** | derivatives, partial derivatives, chain rule, gradients, Jacobians | ✅ `20_Math_and_Statistics_Foundations` |
| **Probability** | distributions, Bayes' theorem, expectation/variance, conditional probability | ✅ `20_Math_and_Statistics_Foundations` |
| **Statistics** | hypothesis testing, confidence intervals, correlation vs causation, sampling | ✅ `20_Math_and_Statistics_Foundations` |
| **Optimization** | convexity, gradient descent, learning rate, local/global minima, SGD variants | 🟡 touched in PyTorch/TF labs Ch.4-5; ⬜ no standalone optimization-theory notebook |

**Dataset examples to practice on:** synthetic linear-regression data (closed-form vs.
gradient-descent solutions), a small covariance/correlation exercise on `retail_sales.csv`.

---

## Level 2 — Data Manipulation (NumPy & Pandas)
**Goal:** array math and real-world tabular data fluency — the bedrock of every later stage.

| Topic | Status |
|---|---|
| ndarray, creation, indexing, broadcasting, vectorization, linear algebra ops | ✅ `NumPy_Zero_to_Master.ipynb` |
| File I/O, random shuffle, partial sort, split, searchsorted, bincount, `numpy.char` | ✅ `NumPy_Additional_Topics.ipynb` |
| DataFrame/Series, `.loc`/`.iloc`, filtering, missing data, cleaning | ✅ `Pandas_Zero_to_Master.ipynb` |
| GroupBy, merge, datetime/resampling, pivot tables | ✅ `Pandas_Zero_to_Master.ipynb` |
| MultiIndex, stack/unstack, `concat`, reading JSON/Excel/GitHub URLs | ✅ `Pandas_Additional_Topics.ipynb` |

**Datasets used:** `retail_sales.csv` (1,010 rows, messy — missing values/dupes/casing),
`weather_2023.csv` (time series), `customers.csv` (merge/join), `student_scores.csv` (NumPy capstone).

---

## Level 3 — Classical Machine Learning
**Goal:** the algorithms that predate deep learning and still power most production systems.

| Topic | Theory | Math | Status |
|---|---|---|---|
| Linear/logistic regression | cost function, decision boundary | least squares, sigmoid, MLE | 🟡 `16_Machine_Learning_Fundamentals` |
| Decision trees & random forests | splitting criteria, ensembling | entropy/Gini, bagging | 🟡 `21_Classical_ML_Advanced` |
| SVMs | max-margin classifiers | kernels, Lagrangian duality | 🟡 `21_Classical_ML_Advanced` |
| k-NN, k-means, clustering | distance-based learning | Euclidean/cosine distance, centroids | 🟡 `16_Machine_Learning_Fundamentals` |
| Naive Bayes | generative classifiers | conditional independence, Bayes' rule | 🟡 `16_Machine_Learning_Fundamentals` |
| Model evaluation | train/val/test split, cross-validation | bias-variance tradeoff | 🟡 `16_Machine_Learning_Fundamentals` |
| Dimensionality reduction | PCA, feature selection | eigendecomposition, variance explained | ✅ covered in the Classical ML lab below |

**Status:** ✅ `Zero_to_Hero_Series/16_Classical_ML_Zero_to_Hero` — full guided lab (theory +
ASCII diagrams + traps + capstone) covering all rows above, verified on the breast-cancer
dataset (96.5% test accuracy across 3 compared models).

**Dataset examples:** `sklearn` toy sets (iris, breast cancer — already used in PyTorch/TF
capstones), `retail_sales.csv` for a regression/classification exercise on real messy data.

---

## Level 4 — Neural Networks & Deep Learning
**Goal:** how neural nets actually compute and learn, from a single neuron to full architectures.

| Topic | Theory | Math | Status |
|---|---|---|---|
| The neuron/perceptron | weighted sum + activation | dot product, step/sigmoid functions | ✅ `17_Neural_Networks_Deep_Dive` |
| Forward pass | layer composition | matrix multiply chains | ✅ `17_Neural_Networks_Deep_Dive/01_Forward_Pass` |
| **Backpropagation** | credit assignment through layers | chain rule, partial derivatives, Jacobians | ✅ `17_Neural_Networks_Deep_Dive/02_Backpropagation` |
| Activation functions | ReLU, sigmoid, tanh, softmax — why nonlinearity matters | derivatives of each, vanishing/exploding gradients | 🟡 touched in PyTorch/TF labs |
| Loss functions | MSE, cross-entropy | log-likelihood, information theory (entropy, KL divergence) | 🟡 touched in PyTorch/TF labs |
| Optimizers | SGD, momentum, Adam | exponential moving averages, adaptive learning rates | 🟡 touched (used, not derived) |
| Regularization | dropout, weight decay, batchnorm | L1/L2 penalties, internal covariate shift | ⬜ not dedicated |
| CNNs | convolution, pooling, receptive fields | convolution as sliding dot-product, parameter sharing | ✅ `17_Neural_Networks_Deep_Dive/03_CNN` |
| RNNs / LSTMs / GRUs | sequence modeling, hidden state, gating | recurrence relations, vanishing gradients over time | ✅ `17_Neural_Networks_Deep_Dive/04_RNN` |
| **PyTorch** (framework) | tensors, autograd, training loop, save/load | — | ✅ `04_PyTorch_Zero_to_Hero` (full lab, verified) |
| **TensorFlow/Keras** (framework) | GradientTape, Sequential/Functional API, callbacks | — | ✅ `TF_Keras_Zero_to_Hero` (full lab, verified) |
| Transformers & attention | self-attention, multi-head attention, positional encoding | scaled dot-product attention (softmax(QKᵀ/√d)V) | ✅ `Zero_to_Hero_Series/11_Transformers_Attention_Zero_to_Hero` (built from raw NumPy, verified mini-GPT capstone) |

**Recommendation:** Transformers/Attention is the most important missing piece — it's the
architecture behind every LLM in this course. Worth a dedicated Zero-to-Hero lab (attention
math, multi-head attention, positional encoding, mini-GPT built from scratch).

**Dataset examples:** Iris & breast-cancer (already used), MNIST-style digit patterns for CNN
intuition, small synthetic sequences for RNN next-token prediction.

---

## Level 5 — Embeddings, Search & Information Retrieval
**Goal:** how text/data becomes vectors, and how to search them at expert depth.

| Topic | Theory | Math/Algorithm | Status |
|---|---|---|---|
| Bag-of-words & tokenization | text → vector | word counting | ✅ `06_Embeddings_Search_Zero_to_Hero` Ch.2 |
| Cosine similarity | direction vs. magnitude | dot product / (‖a‖‖b‖) | ✅ Ch.3 |
| TF-IDF | rarity-weighted keyword search | log-scaled inverse document frequency | ✅ Ch.4 |
| **BM25** | industry-standard ranking | term-frequency saturation (k1), length norm (b) | ✅ Ch.5 |
| Embeddings (conceptual) | meaning → geometry | learned dense vectors, semantic space | ✅ Ch.6 (simulated) |
| **Real embedding models** (expert depth) | how models like `text-embedding-3`, Sentence-BERT are *trained* | contrastive loss, triplet loss, in-batch negatives | ⬜ not covered — currently only *uses* embeddings, doesn't teach how they're trained |
| Hybrid search | fusing keyword + semantic scores | min-max normalization, weighted fusion (α) | ✅ Ch.7 |
| Chunking strategies | fixed-size, overlap, sentence-aware, semantic chunking | sliding window math | ✅ Ch.8 |
| Vector indexes at scale (expert depth) | approximate nearest neighbor search | **HNSW** (hierarchical navigable small worlds), **IVF**, **product quantization**, LSH | ⬜ not covered — current lab uses brute-force cosine, not real ANN algorithms |
| Evaluation | precision@k, recall@k, MRR, nDCG | ranking-quality math | 🟡 Ch.9 covers precision@k/MRR; nDCG not covered |

**Recommendation:** for true "expert level" on embeddings, two things are missing: (1) **how
embedding models are trained** (contrastive learning, why "bad negatives" matter), and (2) **the
actual ANN algorithms** production vector databases use (HNSW graph search, IVF clustering,
quantization) — the current lab teaches brute-force cosine similarity, which is correct
conceptually but not what FAISS/Pinecone/Chroma do internally at scale.

**Dataset examples:** the 10-doc support-ticket corpus (already built), extendable to a larger
100+ doc corpus to make ANN vs. brute-force speed differences tangible.

---

## Level 6 — Large Language Models & Prompting
**Goal:** programming LLMs reliably as an engineer, not just chatting with them.

| Topic | Status |
|---|---|
| API mechanics (messages, roles, statelessness) | ✅ `05_LLM_APIs_Prompting_Zero_to_Hero` Ch.1-2 |
| Sampling (temperature, top_p) | ✅ Ch.3 |
| Prompt patterns: zero-shot, few-shot, chain-of-thought | ✅ Ch.4 |
| Structured output (reliable JSON) | ✅ Ch.5 |
| Conversation memory & context windows | ✅ Ch.6 |
| Cost/token budgeting | ✅ Ch.7 |
| Error handling & retries | ✅ Ch.8 |
| **How transformers generate text** (expert depth) | ⬜ not covered — tokenization (BPE), next-token prediction loop, logits→sampling internals live under Level 4's Transformer gap |
| **Fine-tuning vs. prompting vs. RAG** (when to use which) | ⬜ not covered as an explicit decision framework |

**Dataset examples:** the ticket-triage corpus (billing/technical/shipping/account) used
throughout, offline via `MockLLM` — swappable to real OpenAI/Gemini clients.

---

## Level 7 — Retrieval-Augmented Generation (RAG)
| Topic | Status |
|---|---|
| Why RAG (hallucination problem) | ✅ `07_RAG_Zero_to_Hero` Ch.1 |
| Full pipeline: ingest→chunk→embed→index→retrieve→generate | ✅ Ch.2-7 |
| Guardrails: similarity threshold, "I don't know" | ✅ Ch.8 |
| RAG evaluation (retrieval hit-rate + answer grounding) | ✅ Ch.9 |
| **Advanced RAG** (expert depth): query rewriting, re-ranking (cross-encoders), multi-hop retrieval, HyDE | ⬜ not covered — current lab is single-pass retrieve-then-generate |
| Production vector DBs (Chroma/FAISS/Pinecone specifics) | ⬜ referenced conceptually, not hands-on with a real DB |

---

## Level 8 — Orchestration Frameworks & Agents
| Topic | Status |
|---|---|
| LangChain: Runnables, LCEL pipe, prompt templates, parsers, memory, tools | ✅ `08_LangChain_Zero_to_Hero` |
| Agent vs. chain, ReAct loop (Reason→Act→Observe) | ✅ `09_Agents_Orchestration_Zero_to_Hero` Ch.1-4 |
| Tool selection, agent memory, loop safety | ✅ Ch.5-7 |
| Human-in-the-loop approval gates | ✅ Ch.8 |
| Multi-agent orchestration (planner + workers) | ✅ Ch.9-10 |
| MCP (Model Context Protocol): host/client/server, tools/resources/prompts | ✅ `12_MCP_Tooling_Zero_to_Hero` |
| **A2A Protocol** (agent-to-agent communication) | ✅ `Zero_to_Hero_Series/13_A2A_Protocol_Zero_to_Hero` (Agent Cards, discovery, task lifecycle, delegation — verified capstone) |
| Agent evaluation (task success rate, trajectory analysis) | ⬜ not covered |

---

## Level 9 — Evaluation, Guardrails & Safety
| Topic | Status |
|---|---|
| Eval sets, accuracy, keyword scoring | ✅ `10_Evaluation_Guardrails_Zero_to_Hero` Ch.1-3 |
| Precision/recall/F1, macro-F1 | ✅ Ch.4 |
| LLM-as-judge | ✅ Ch.5 |
| Input guardrails (injection, PII detection) | ✅ Ch.6 |
| Output guardrails (format validation, PII redaction) | ✅ Ch.7 |
| Regression testing | ✅ Ch.8 |
| **Red-teaming / adversarial testing** (expert depth) | ⬜ not covered |
| **Constitutional AI / RLHF concepts** (how models are aligned) | ⬜ not covered |

---

## Level 10 — Production & MLOps
| Topic | Status |
|---|---|
| Data engineering, pipelines | 🟡 `24_Data_Engineering_and_MLOps` (exercises exist, no zero-to-hero lab) |
| Software engineering tooling (testing, CI/CD, packaging) | 🟡 `25_Software_Engineering_Tooling` |
| Model serving, latency/cost tradeoffs at scale | ⬜ not covered |
| Monitoring & observability for LLM apps (drift, logging, tracing) | ⬜ not covered |

---

## 🗺️ Status Update — All 7 Gaps Closed ✅

Every gap identified in the original curriculum audit is now **built, verified, and folded into
`Zero_to_Hero_Series/`**: A2A Protocol, Transformers & Attention, Classical ML, Vector Search at
Scale, Embedding Model Training, Advanced RAG, and MLOps & Production Serving. The Zero-to-Hero
series is now **16 modules**, all inside the one organized archive, with the complete beginner-
to-expert path covering theory, math, algorithms, ASCII diagrams, worked examples, exercises,
solutions, and a verified capstone in every module.

| Closed gap | Module |
|---|---|
| Transformers & Attention | `11_Transformers_Attention_Zero_to_Hero` |
| Classical ML | `16_Classical_ML_Zero_to_Hero` |
| A2A Protocol | `13_A2A_Protocol_Zero_to_Hero` |
| Vector Search at Scale (HNSW/IVF/LSH/PQ) | `17_Vector_Search_at_Scale_Zero_to_Hero` |
| Embedding Model Training (contrastive/triplet loss) | `18_Embedding_Model_Training_Zero_to_Hero` |
| Advanced RAG (re-ranking, HyDE, multi-hop) | `19_Advanced_RAG_Zero_to_Hero` |
| MLOps & Production Serving | `20_MLOps_Production_Serving_Zero_to_Hero` |

## What's Genuinely Still Open (beyond this course's scope)

A few topics are large enough to be their own specialization rather than a single lab — flagging
honestly rather than claiming false completeness:
- **Distributed training** (multi-GPU/multi-node, DeepSpeed/FSDP) — how billion-parameter models
  are actually trained across hardware clusters.
- **Model compression for deployment** (quantization to INT8/INT4, distillation, pruning) beyond
  the PQ vector-compression already covered.
- **Formal RLHF/Constitutional AI implementation** — the alignment training pipeline itself
  (reward modeling, PPO), as opposed to the conceptual overview already in the curriculum.
- **Red-teaming / adversarial robustness testing** as a dedicated discipline.

These are reasonable "PhD-adjacent" extensions if you want to go further — say the word and I'll
scope and build any of them the same way.
