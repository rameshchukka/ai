# Module 6 — Diagrams

## 1. Host / Client / Server architecture

```
 ┌─────────────────────────────────────────┐
 │  HOST (your agent application)            │
 │   ┌───────────────────────────────────┐  │
 │   │  MCP CLIENT                        │  │
 │   └─────────────┬─────────────────────┘  │
 └─────────────────┼──────────────────────┘
                    | MCP protocol (stdio or HTTP/SSE)
        ┌───────────┼────────────┬────────────┐
        v           v            v            v
  ┌──────────┐┌──────────┐┌──────────┐┌──────────┐
  │ MCP Server││ MCP Server││ MCP Server││ MCP Server│
  │ (retriever)││ (SQL DB)  ││(filesystem)││(calc tool)│
  └──────────┘└──────────┘└──────────┘└──────────┘

  One host <-> many servers. Each server is independent,
  reusable by any other MCP-compliant host.
```

## 2. The three primitives, who controls what

```
                       MCP Server exposes:
                              |
        ┌─────────────────────┼─────────────────────┐
        v                     v                     v
     Tools                Resources               Prompts
  (model-controlled)   (app-controlled)        (user-controlled)
        |                     |                     |
  model decides          host attaches          user explicitly
  when to call            to context as          invokes a template
  e.g. search_docs()      needed, e.g. a file     e.g. "/summarize"
```

## 3. Message flow, one tool call (stdio transport)

```
  Host process                         Server process (subprocess)
  ───────────                          ───────────────────────────
       |  spawn subprocess, open stdio pipe  |
       |───────────────────────────────────> |
       |  initialize handshake                |
       |<─────────────────────────────────── |
       |  list_tools()                        |
       |───────────────────────────────────> |
       |<─────────────────────────────────── |  [returns tool schemas]
       |  (LLM decides to call a tool)        |
       |  call_tool("search_docs", {...})     |
       |───────────────────────────────────> |
       |                                       |  [server executes]
       |<─────────────────────────────────── |  tool result
       |  (result fed back into LLM context)  |
```

## 4. Reuse: same server, different hosts

```
  MCP Server: "retriever_tool"
        ^              ^
        |              |
  ┌──────────┐    ┌──────────┐
  │ Your      │    │ Teammate's│
  │ Python     │    │ different  │
  │ agent      │    │ framework  │
  │ (LangChain)│    │ (any lang) │
  └──────────┘    └──────────┘

  Neither host needs to know HOW the server is implemented —
  only that it speaks MCP.
```
