# 🔌 MCP & Tooling: Zero to Hero — Guided Lab

Understand the Model Context Protocol (MCP) — the open standard that connects LLM apps to tools, data, and prompts through one uniform interface. Build a working MCP server and client from scratch: tools, resources, prompts, discovery, invocation, and agent wiring. 100% offline; concepts map directly to the real MCP SDK.

## The teaching format (every chapter)
- 📖 **Theory** (detailed) — the concept explained properly, not just name-dropped
- 🧠 **Mental model** — the intuition to hold in your head
- 🖼️ **ASCII diagram** — a visual of how it fits together
- 🔬 **Worked example** — runnable code you execute and read
- ⚡ **Pro tips** and ⚠️ **Common traps** — what actually trips people up
- ✏️ **Your Turn** exercise → ✅ **Solution** (revealed right after)

## Chapters
1. What MCP is & why it exists
2. Architecture: host, client, server
3. The three primitives: tools, resources, prompts
4. Building an MCP server (tools)
5. Tool schemas & discovery
6. Resources (exposing data)
7. Prompts (reusable templates)
8. The client: discovering & calling
9. Wiring MCP into an agent
10. 🏆 Capstone: complete MCP server + agent

## Requirements
```
pip install --upgrade pip   # no external deps; the real SDK is: pip install mcp
```

We build minimal in-memory MCP primitives with the same shape as the real protocol; the final chapter points to the official `mcp` SDK.

Work top to bottom. Attempt every ✏️ exercise before opening its ✅ solution, and finish with
the 🏆 capstone.
