# Phase 2 — Diagrams

## 1. Fixed-size vs Recursive vs Semantic, same paragraph

```
TEXT: "Authentication requires an API key. The key must be sent in the
       Authorization header. Requests without it return 401. Error codes
       are documented below. 404 means not found, 500 means server error."

FIXED-SIZE (cuts blindly every N chars):
  [Authentication requires an API key. The key must be] | [sent in the
  Authorization header. Requests without it return 401] | [...]
  ^ cuts mid-sentence, ignores meaning entirely

RECURSIVE (tries paragraph, then sentence boundary):
  [Authentication requires an API key. The key must be sent in the
   Authorization header. Requests without it return 401.]
  [Error codes are documented below. 404 means not found, 500 means
   server error.]
  ^ respects sentence boundaries, but still split by length not topic

SEMANTIC (splits where embedding similarity drops):
  [Authentication requires an API key. The key must be sent in the
   Authorization header. Requests without it return 401.]
  [Error codes are documented below. 404 means not found, 500 means
   server error.]
  ^ happens to agree with recursive here, but would diverge on text where
    sentence boundaries don't align with topic boundaries
```

## 2. Structure-aware chunking on Swagger/JSON

```
  openapi.yaml
    paths:
      /payments:
        get:   ──────────> CHUNK 1: GET /payments (full operation object)
        post:  ──────────> CHUNK 2: POST /payments (full operation object)
      /payments/{id}:
        get:   ──────────> CHUNK 3: GET /payments/{id}

  Never splits a single operation's parameters from its responses —
  the YAML/JSON structure itself defines the chunk boundary.
```

## 3. Hierarchical chunking, queryable at multiple levels

```
                    Book
                      |
        ┌─────────────┼─────────────┐
        v              v              v
    Chapter 1      Chapter 2      Chapter 3
        |
   ┌────┴────┐
   v          v
 Section 1.1  Section 1.2
   |
   v
 Paragraph

 Broad question ("what is this book about?")     -> retrieve at Chapter level
 Narrow question ("what does section 1.2 say?")   -> retrieve at Paragraph level
 Same source document, different retrieval granularity depending on the question
```

## 4. Parent-child chunking, done correctly vs incorrectly

```
 CORRECT:
   embed CHILD chunks individually --> ["Authentication", "Headers",
                                         "Request", "Response", "Errors"]
   each child stores a pointer: parent_id = "customer_search_api"
   query "auth header format" --> matches "Authentication" child (best similarity)
                                --> return ANCESTOR/parent doc for full context

 INCORRECT (common mistake):
   embed the PARENT text directly: "Customer Search API: Authentication...
   Headers... Request... Response... Errors..." (everything concatenated)
   query "auth header format" --> matches the one blob (broad, imprecise)
                                --> returns same noisy blob every time,
                                    indistinguishable from plain fixed-size chunking
```

## 5. Graph chunking — when text isn't linear

```
  Linear chunk (loses the relationship):
  "Service A calls Service B. Service B depends on Service C for auth."

  Graph representation (keeps the relationship queryable):

      [Service A] --calls--> [Service B] --depends_on--> [Service C]
                                                              |
                                                          (auth)

  Query: "what does Service A ultimately depend on for auth?"
  Graph traversal: A -> B -> C, follow "depends_on" edge labeled "auth"
  -- a linear chunk store has no native way to answer a multi-hop
     relationship question like this; a graph does.
```
