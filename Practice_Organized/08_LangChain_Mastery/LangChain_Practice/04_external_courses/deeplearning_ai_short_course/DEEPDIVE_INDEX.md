# Deep-Dive Guides — DeepLearning.AI LangChain Course

A per-notebook deep dive: the concepts explained, then the actual code walked through
block by block (what each construct does and why).

| Notebook | Deep dive | Covers |
|---|---|---|
| L1 | `DEEPDIVE_L1.html` | Models, prompt templates, output parsers (text → dict) |
| L2 | `DEEPDIVE_L2.html` | Memory: buffer / window / token / summary + trade-offs |
| L3 | `DEEPDIVE_L3.html` | Chains: LLMChain, SimpleSequential, Sequential, Router |
| L4 | `DEEPDIVE_L4.html` | RAG over documents — one-liner vs the full manual pipeline |
| L5 | `DEEPDIVE_L5.html` | Evaluation: generate tests, debug trace, LLM-as-judge |
| L6 | `DEEPDIVE_L6.html` | Agents: built-in tools, Python agent, custom @tool, ReAct |

**How to use:** open the deep dive for a notebook alongside the notebook itself. Read the
concept, then run the matching cell and compare with the code explanation.

Setup for actually running the notebooks (Python, venv, versions, keys) is in
`DEVELOPER_GUIDE_beginner.html`. Remember these notebooks use the OLD LangChain/OpenAI
APIs — pin `langchain==0.0.312` and `openai==0.28.1`, or use the modern-imports table in
the beginner guide.
