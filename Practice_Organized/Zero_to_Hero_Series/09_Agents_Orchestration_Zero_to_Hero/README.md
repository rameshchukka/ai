# 🤖 Agents & Orchestration: Zero to Hero — Guided Lab

Build LLM agents from scratch: the ReAct loop (Reason->Act->Observe), tools with schemas, tool selection, working vs long-term memory, loop-safety guards, human approval gates, and multi-agent orchestration. 100% offline with a mock reasoner; the control flow matches real agent frameworks.

## The teaching format (every chapter)
- 📖 **Theory** (detailed) — the concept explained properly, not just name-dropped
- 🧠 **Mental model** — the intuition to hold in your head
- 🖼️ **ASCII diagram** — a visual of how it fits together
- 🔬 **Worked example** — runnable code you execute and read
- ⚡ **Pro tips** and ⚠️ **Common traps** — what actually trips people up
- ✏️ **Your Turn** exercise → ✅ **Solution** (revealed right after)

## Chapters
1. Agent vs chain (why agents?)
2. Tools with schemas
3. The ReAct loop
4. Single-tool agent
5. Multi-tool agents & tool selection
6. Agent memory & scratchpad
7. Stopping conditions & loop safety
8. Human-in-the-loop approval gates
9. Multi-agent orchestration
10. 🏆 Capstone: orchestrated research assistant

## Requirements
```
pip install --upgrade pip   # no external deps required
```

Prerequisite: the LangChain lab. Swap the mock reasoner for a real LLM (prompted to emit the next action as JSON) to go live.

Work top to bottom. Attempt every ✏️ exercise before opening its ✅ solution, and finish with
the 🏆 capstone.
