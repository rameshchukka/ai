# Capstone Scaffold

This is the working starting point for your Month 6 capstone build sprints — deliberately
minimal so you spend Lab 5 on scoping, not infrastructure.

## Structure

```
capstone_scaffold/
  src/main.py       - entry point + health check (replace with your real logic)
  data/             - put your capstone's documents/datasets here
  tests/            - test_main.py is a placeholder, expand in Month 6
  llm_client.py     - same Gemini/OpenRouter/mock wrapper as every other lab
  requirements.txt
  .env.example
```

## Setup

```bash
cd capstone_scaffold
pip install -r requirements.txt
cp .env.example .env
# fill in your keys, set LLM_PROVIDER=gemini_auto
python src/main.py     # should print "Scaffold structure OK. Ready for Month 6 build sprints."
```

## What to do with this in Month 6

Replace `src/main.py`'s trivial health check with your actual capstone's entry point,
reusing the patterns from Labs 1-4 as building blocks:
- RAG ingestion/retrieval (Lab 2's `chunking.py`/`ingest.py`/`retrieve.py`/`generate.py` pattern)
- Agent loop with tools (Lab 3's `agent.py`/`tools.py` pattern)
- Eval suite + guardrails (Lab 4's `eval_runner.py`/`guardrails.py` pattern)

This scaffold intentionally doesn't pre-build any of that for you — Lab 5 is about proving
the plumbing works, not building the capstone itself.
