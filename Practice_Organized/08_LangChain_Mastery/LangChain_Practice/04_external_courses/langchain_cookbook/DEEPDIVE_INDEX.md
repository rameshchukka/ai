# Deep-Dive Guides — LangChain Cookbook

Four deep-dive guides covering all ~28 notebooks, grouped logically. Each explains the
concepts and walks the real code, with a "practice" pointer.

| Guide | Covers | Start here if… |
|---|---|---|
| `DEEPDIVE_Part1_Fundamentals.html` | the 6 component families (schema, models, prompts, indexes/RAG, memory, chains, agents) | you're new — **do this first** |
| `DEEPDIVE_Part2_UseCases.html` | shippable use cases: summarization, RAG Q&A, extraction, evaluation, tabular, code, APIs, chatbots, agents | you want to see what to build |
| `DEEPDIVE_Core_Folders.html` | chains (document strategies), agents (tools/ReAct/Zapier), loaders (YouTube/Drive), chatapi, bots | you want depth on one component |
| `DEEPDIVE_Applied_Recipes.html` | 14 real recipes in data_generation/ (summarization levels, Ask-A-Book, MMR, structured output, tone, transcripts) | you want reusable, real-world code |

## Recommended path
1. **Part 1 Fundamentals** — run the notebook alongside the guide; it's a runnable glossary.
2. **Part 2 Use Cases** — see the blocks assembled into real tasks.
3. **Applied Recipes** — do the three headliners (5 Levels of Summarization, Ask A Book, MMR),
   then pick recipes matching your work.
4. **Core Folders** — dip in when you need depth on chains / agents / loaders.

## Setup (once)
```
pip install langchain openai faiss-cpu chromadb tiktoken
export OPENAI_API_KEY=your-key         # or swap for your in-house wrapper
```
Data ships in `data/` (Paul Graham essays, CSVs). Some recipes need extra packages/keys
(Pinecone, Zapier, Kor, YouTube tools) — each notebook lists them at the top.

## Version note (important)
These notebooks use the **older `langchain.*` import paths** (e.g.
`from langchain.chat_models import ChatOpenAI`). On current LangChain, imports moved to
`langchain_openai` / `langchain_community`, and old `openai.ChatCompletion` calls changed.
If an import errors: either `pip install "langchain<0.1" "openai<1"` to run them as-is, or
update the import to the current path (the concept is unchanged). The deep-dive guides
explain the concepts, which don't change across versions.
