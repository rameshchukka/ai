# 💬 LLM APIs & Prompting: Zero to Hero — Guided Lab

Program LLMs (GPT/Gemini) like an engineer: roles, sampling, prompt patterns, reliable structured output, conversation memory, cost budgeting, and robust retries. Runs 100% offline with a MockLLM; swap in a real client with one line.

## The teaching format (every chapter)
- 📖 **Theory** (detailed) — the concept explained properly, not just name-dropped
- 🧠 **Mental model** — the intuition to hold in your head
- 🖼️ **ASCII diagram** — a visual of how it fits together
- 🔬 **Worked example** — runnable code you execute and read
- ⚡ **Pro tips** and ⚠️ **Common traps** — what actually trips people up
- ✏️ **Your Turn** exercise → ✅ **Solution** (revealed right after)

## Chapters
1. How an LLM API call works
2. Roles: system/user/assistant
3. Sampling (temperature, top_p)
4. Prompt patterns: zero-shot, few-shot, chain-of-thought
5. Structured output (reliable JSON)
6. Conversation state & context windows
7. Cost & token budgeting
8. Error handling & retries
9. A mini application (auto-tagger)
10. 🏆 Capstone: robust ticket-triage pipeline

## Requirements
```
pip install --upgrade pip   # no external API needed; optional: openai, google-generativeai
```

Everything runs offline. The final chapter shows the exact one-line swap to real OpenAI/Gemini clients.

Work top to bottom. Attempt every ✏️ exercise before opening its ✅ solution, and finish with
the 🏆 capstone.
