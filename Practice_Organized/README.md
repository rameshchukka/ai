# Python & AI Course — Organized by Learning Section

Your original `Practice.zip` has been unpacked and regrouped into one numbered learning
path. On top of the original course files, every applied section (03–11, 15) now has a
`Real_World_Exercises/` folder with new hands-on notebooks, plus a **Developer Guide**
(technical reference) and a **User Guide (Brain-Friendly)** (plain-language walkthrough)
covering what you'll learn and important tips before you start. Four sections that were
missing from the original material have also been added (16–19).

## ⭐ Zero to Hero Series & Master Curriculum

- **`Zero_to_Hero_Series/`** — 16 standalone, deeply-taught modules covering the **complete**
  basics-to-expert path: PyTorch, TensorFlow/Keras, Classical ML, Transformers & Attention, LLM
  APIs, Embeddings & Search, Vector Search at Scale, Embedding Model Training, RAG, Advanced RAG,
  LangChain, Agents & Orchestration, MCP, A2A Protocol, Evaluation & Guardrails, and MLOps &
  Production Serving. Each has detailed theory, ASCII diagrams, mental models, pro tips, traps,
  exercises + solutions, and a verified capstone. See `Zero_to_Hero_Series/README.md` for the
  recommended learning order.
- **`MASTER_CURRICULUM.md`** (this folder) — the complete basics-to-expert course map with
  theory/math/algorithm breakdowns per topic, dataset examples, and full status (all prior gaps
  now closed).
- **`Concept_Guides/`** — 9 short, reading-first PDF guides (no code) for every math/algorithm-
  heavy topic: NumPy & Linear Algebra, Math & Statistics Foundations, Classical ML, Neural
  Networks & Backpropagation, Training Math, Transformers & Attention, Embeddings & Search,
  Vector Search at Scale, and Embedding Model Training. Each has the concept in plain English,
  the formula built up term by term, a hand-worked numeric example, a mental model, and common
  misunderstandings — read one before its matching notebook. See `Concept_Guides/README.md`.
- **External practice courses** — three external course repos you uploaded (Python
  Fundamentals, Python for Data Science, Google Colab for Data Science & AI), reviewed,
  verified, and fixed where genuinely broken — then **distributed by topic** into the
  numbered sections above rather than kept separate, so each lesson sits next to the
  content it's most related to:
  - `01_Python_Basics/External_Python_Fundamentals_Course/` — all 10 lessons (basics through exceptions)
  - `01_Python_Basics/External_Python_for_DataScience_Course/` — basics-level lessons
  - `02_Python_Advanced_and_Exercises/External_Python_for_DataScience_Course/` — functional programming, lazy evaluation, pattern matching, I/O
  - `19_Algorithms_and_Data_Structures/External_Python_for_DataScience_Course/` — sorting
  - `03_Data_Science_NumPy_Pandas/External_Python_for_DataScience_Course/` — case studies
  - `03_Data_Science_NumPy_Pandas/External_Google_Colab_DataScience_Course/` — all 9 exercise modules + real dataset

## Structure

| # | Folder | What's inside |
|---|--------|----------------|
| 01 | `01_Python_Basics` | Variables, Lists, Tuples, Sets, Dictionaries, Control Flow, Imports/Modules, Functions, OOPs |
| 02 | `02_Python_Advanced_and_Exercises` | Core fundamentals notebooks + 12 practice-exercise notebooks (OOP, async, multithreading, testing, FastAPI, SQL, Git, Docker, Linux) |
| 03 | `03_Data_Science_NumPy_Pandas` | **⭐ Zero_to_Master_Lab (complete beginner→expert guided course for NumPy & Pandas, with theory + real datasets + exercises inside the notebooks)**, NumPy/Pandas Modules 1–4, extra data-science practice, Real_World_Exercises + guides |
| 04 | `04_Deep_Learning_PyTorch` | PyTorch `nn.Module` notebook **+ Real_World_Exercises (tensors, autograd, full training loop, house-price regression) + guides** |
| 05 | `05_LLM_APIs_and_Prompting` | OpenAI/Gemini API basics, Gemini prompting lab, LLM Fundamentals Lab **+ Real_World_Exercises (structured output, few-shot, context management, retries) + guides** |
| 06 | `06_Embeddings_and_Search` | Embeddings notebooks, TF-IDF/BM25/semantic/hybrid search exercises **+ Real_World_Exercises (build a search engine from scratch) + guides** |
| 07 | `07_RAG_Retrieval_Augmented_Generation` | RAG Pipeline Lab, RAG Visualizer, Chroma lab, 9-phase RAG Specialist Track **+ Real_World_Exercises (full RAG pipeline + hallucination guardrail) + guides** |
| 08 | `08_LangChain` | Core LangChain scripts + 2 extension notebook sets **+ Real_World_Exercises (PromptTemplate, LCEL chains, memory, tools) + guides** |
| 09 | `09_Agents_and_Orchestration_week16` | Agent orchestration lab **+ Real_World_Exercises (ReAct loop built from scratch, approval gating) + guides** |
| 10 | `10_Evaluation_and_Guardrails_week17` | Eval runner, LLM judge, guardrails, regression tests **+ Real_World_Exercises (eval harness, LLM-as-judge, input/output guardrails) + guides** |
| 11 | `11_Capstone_week18` | Capstone kickoff templates and scaffold **+ Real_World_Exercises (scoping/discovery/MVP-cut exercise) + guides** |
| 12 | `12_MCP_and_Tooling` | MCP code examples/demo + MCP practice notebooks (incl. KYC AI guides) |
| 13 | `13_Mini_Project_Verification_Analyzer` | Standalone verification-analyzer mini project docs |
| 14 | `14_Multimodal_Test_Assets` | Sample image/audio/video test files used across labs |
| 15 | `15_AI_Mastery_Full_Track_00to09` | Parallel end-to-end syllabus (foundations → productionizing) **+ Real_World_Exercises (end-to-end pipeline integration) + guides** |
| 16 | `16_Machine_Learning_Fundamentals` **(new)** | Classical ML: regression, trees, clustering, bias/variance, metrics — with a churn-prediction exercise notebook + guides |
| 17 | `17_Neural_Networks_Deep_Dive` **(new)** | Forward pass, backpropagation, CNN, RNN — each with a from-scratch exercise notebook + guides |
| 18 | `18_Generative_AI_Fundamentals` **(new)** | Tokenization, self-attention (built from scratch in NumPy), autoregressive sampling/temperature + guides |
| 19 | `19_Algorithms_and_Data_Structures` **(new)** | Big-O, hash maps, sorting/searching, graph traversal (BFS), dynamic programming + guides |
| 20 | `20_Math_and_Statistics_Foundations` **(new)** | Linear algebra, probability distributions, Bayes' theorem, hypothesis testing, gradients, A/B testing + guides |
| 21 | `21_Classical_ML_Advanced` **(new)** | SVM, Naive Bayes, gradient boosting, PCA, hyperparameter tuning (GridSearchCV), classical time series (ARIMA) + guides |
| 22 | `22_Deep_Learning_Advanced` **(new)** | Multi-head attention/Transformer blocks, dropout/batch norm, autoencoders, GANs, reinforcement learning (Q-learning) + guides |
| 23 | `23_GenAI_LLM_Advanced` **(new)** | FAISS vector search, re-ranking, LLM observability/tracing, prompt-injection defense, knowledge graphs + guides |
| 24 | `24_Data_Engineering_and_MLOps` **(new)** | ETL pipelines, DAG orchestration, model registry/versioning, effective visualization, SQL window functions + guides |
| 25 | `25_Software_Engineering_Tooling` **(new)** | REST API design, caching (LRU), message queues, design patterns, heaps/tries, regex + guides |

## Suggested order

1. **Python fundamentals**: 01 → 02
2. **Data foundations**: 03 → 04, with `16_Machine_Learning_Fundamentals` as a good bridge before/after 04
3. **Neural network internals** (optional deep-dive, recommended before or alongside 04): `17_Neural_Networks_Deep_Dive`
4. **GenAI/LLM track**: `18_Generative_AI_Fundamentals` → 05 → 06 → 07 → 08 → 09 → 10 → 11
5. **Supporting material**: 12, 13, 14 (reference/tooling/assets, use as needed)
6. **Optional deep-dive**: 15 is a self-contained parallel syllabus covering the same GenAI ground in more depth
7. **Anytime reference**: `19_Algorithms_and_Data_Structures` — dip into this whenever you want a CS-fundamentals refresher
8. **Going deeper / filling gaps (20–25)**: once comfortable with the core path, layer in `20_Math_and_Statistics_Foundations` (useful early, alongside 03–04), `21_Classical_ML_Advanced` and `22_Deep_Learning_Advanced` (after 16/17), `23_GenAI_LLM_Advanced` (after 07–09), `24_Data_Engineering_and_MLOps` and `25_Software_Engineering_Tooling` (whenever you're ready to productionize a project, e.g. alongside 11)

## How each exercise folder works

Open **`Exercise_Guides_Index.html`** (at the root of this course) in your browser for a
clickable index of every exercise guide. Each exercise-bearing folder (03–11, 15–19) contains:

- **`Exercise_Guide_*.html`** — an interactive, beginner-friendly HTML guide for that
  specific exercise notebook, with four sections:
  1. **📘 Concept Notes** — plain-language explanations of the underlying ideas
  2. **🧭 Beginner → Expert Roadmap** — a 3-tier checklist so you know what "good" looks like at each stage
  3. **🛠️ Exercise Walkthrough** — every `TODO` in the notebook, explained (why it matters + what concept it tests), with a click-to-reveal hint
  4. **💡 Tips & Pitfalls** and **🌍 Real-World Use Cases**
- **`Developer_Guide.md`** — the technical-reference version of the same tips/pitfalls/use-cases, for quick markdown reading (e.g. on GitHub).
- **`User_Guide_BrainFriendly.md`** — the plain-language markdown version with a recommended study flow.
- **One or more exercise notebooks** — worked examples + `# TODO` exercises you attempt yourself, each with a collapsible `<details>` solution underneath so you can self-check without spoiling the answer up front.

**Recommended flow:** open the HTML guide first → skim Concept Notes → check where you
land on the roadmap → open the notebook and work through it, using the guide's hints
(not the notebook's built-in solutions) as your first fallback → only reveal the full
notebook solution if still stuck.

Weeks 14–18 labs (folders 05, 07, 09, 10, 11) each also include their own original
`README.md`, `GEMINI_NOTES.md`, and `OPENROUTER_NOTES.md` with setup instructions.

## A note on requirements

Some new exercises use `torch` and `scikit-learn`. Install if needed:
```
pip install torch scikit-learn --break-system-packages
```
LLM/RAG/LangChain/Agent exercises are written to run fully offline with mocked clients
so you can learn the patterns without API keys — swap in a real client using the same
interface once you're ready.
