# Gap Fillers — The Depth That Makes You Expert

Your existing material covers every *topic* in `Expert_Rag.txt`. These three
notebooks add the *practice depth* that separates "understands RAG" from "expert
at RAG." All three run **fully offline** (mock embedder + mock LLM, no API key,
no network) — and all three were **executed and verified to run clean**, not just
syntax-checked. Swap the mock for your real `InHouseEmbeddings` + `ask()` to make
them real.

## 1. `01_advanced_patterns_runnable.ipynb`
Your Specialist Track phase6 covers the RAG patterns as concept notes. This makes
the four hardest ones **executable so you can watch them behave**:
- **Corrective RAG (CRAG)** — checks retrieval quality, refuses/falls back when weak
- **Adaptive RAG** — routes by query type (simple vs comparison vs multi-part) before retrieving
- **Multi-hop RAG** — decomposes a compound question, retrieves per sub-question, combines
- **Fusion RAG** — multiple query rephrasings fused with Reciprocal Rank Fusion

The point: pattern logic is separate from model plumbing. Same logic works with a
mock or your real Jina/LLM — only the embed/generate calls change.

## 2. `02_evaluation_harness.ipynb`
Your material covers each metric separately. Expert practice is running them
**together, on the same dataset, to compare retrievers head-to-head**:
- Precision@K, Recall@K, MRR, NDCG@K — all in one place, on one labeled benchmark
- A head-to-head comparison (k=1 vs k=3) showing the precision/recall tradeoff numerically
- Extension prompts for adding Answer Faithfulness via LLM-as-judge

This is the notebook you'll reuse every time you change *anything* (embedding
model, chunk size, retriever) to prove the change actually helped.

## 3. `03_production_tuning.ipynb`
The experiments most tutorials skip and experts always run:
- **Chunk size sweep** — watch retrieval quality change as chunk size varies
- **Overlap experiment** — prove overlap rescues answers sitting at chunk boundaries
- **Retrieval failure analysis** — the single most useful debugging habit: read the
  ranked retrieval list with scores, because most "bad LLM answer" bugs are actually
  "retrieved the wrong chunk" bugs

Ends with the capstone tuning loop: sweep chunk_size × overlap × k against a
labeled benchmark and pick the config with the best NDCG — data-driven, not vibes.

## How to make these real
Every notebook starts with a `MOCK` cell defining `MockEmbedder` and `mock_llm`.
Replace those two with:
```python
from inhouse_wrappers import InHouseEmbeddings, get_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
embedder = InHouseEmbeddings()
def ask(system, user, **kw):
    llm = get_chat_model()
    return llm.invoke([SystemMessage(content=system), HumanMessage(content=user)]).content
mock_llm = ask
```
Nothing else in any notebook needs to change.
