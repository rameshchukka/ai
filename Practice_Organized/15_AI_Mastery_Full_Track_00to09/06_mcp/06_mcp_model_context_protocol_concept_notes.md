# Module 6 — MCP (Model Context Protocol)

## 1. Why MCP exists
Before MCP, every AI app wrote custom integration code for every tool/data
source it wanted an LLM to use. MCP standardizes that interface: any
MCP-compliant **client** (your agent/app) can talk to any MCP-compliant
**server** (a tool/data provider) without bespoke glue code — analogous to
how USB standardized device connections instead of every device needing its
own port.

## 2. Architecture: Host, Client, Server
| Role | What it is | Example |
|---|---|---|
| Host | The application the user interacts with | Claude Desktop, your custom agent app |
| Client | The MCP protocol implementation inside the host | Library code that speaks MCP |
| Server | A process exposing tools/data via MCP | A server wrapping your retriever, a database, a filesystem |

One host can connect to many servers simultaneously; one server can serve
many clients.

## 3. The three primitives
| Primitive | Direction | Analogy | Example |
|---|---|---|---|
| Tools | Model calls these (model-controlled) | Functions | `search_documents(query)`, `run_sql(query)` |
| Resources | Host/user reads these (app-controlled) | Files/data the app can attach to context | A document, a database schema |
| Prompts | User-invoked templates (user-controlled) | Slash-commands / pre-built prompt templates | "/summarize-this-doc" |

## 4. Transports
| Transport | How it connects | Use when |
|---|---|---|
| stdio | Server runs as a local subprocess, communicates via stdin/stdout | Local tools, desktop apps, simplest setup |
| SSE / HTTP (Streamable HTTP) | Server runs as a network service | Remote servers, multi-client access, cloud deployment |

## 5. How this connects to your earlier agent notebooks
Your manual ReAct loop (Module 5) hand-rolled the "model proposes action →
code executes → feed back" cycle with Python functions directly in-process.
MCP formalizes exactly that cycle but makes the tool side a **separate
process/service** speaking a standard protocol — so the same tool server
could be reused by a completely different agent/app without rewriting it.

## Teaser problem
> You wrote a great retriever function for Module 3's RAG pipeline. A
> teammate building a totally different agent (different framework, maybe
> even different language) wants to reuse your retrieval logic without
> copy-pasting your Python code. What's the MCP-native way to share it?

**Solution:** wrap the retriever as an MCP **Tool** on a small MCP server
(stdio or HTTP transport). Your teammate's agent, regardless of framework,
just needs an MCP client pointed at your server — no shared codebase, no
language constraint, just the protocol. See the worksheet notebook in this folder for a minimal
working MCP server exposing exactly this.
