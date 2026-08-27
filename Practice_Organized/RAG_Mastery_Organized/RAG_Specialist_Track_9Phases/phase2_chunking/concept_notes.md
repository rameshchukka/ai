# Phase 2 — Chunking (the most important phase)

## Why beginners get this wrong
Splitting purely by character count is the easiest thing to implement and the
worst thing for retrieval quality — it cuts sentences and ideas in half with no
regard for meaning. Every strategy below exists to fix a specific failure mode of
naive fixed-size splitting.

## The 8 strategies
| Strategy | How it splits | Best for | What naive splitting gets wrong that this fixes |
|---|---|---|---|
| Fixed-size | Every N tokens (e.g. 500, 100 overlap) | Books, generic PDFs with no clear structure | Nothing — it's the baseline everything else improves on |
| Recursive | Tries heading → paragraph → sentence → word, in that order, until chunks fit | Documentation | Cuts mid-sentence; recursive tries larger boundaries first |
| Semantic | Splits where embedding similarity between adjacent sentences drops | Long-form prose, no structure | Splits topically-related content that happens to cross an arbitrary character count |
| Structure-aware | Follows the document's own structure (Swagger endpoints, JSON objects, SQL statements, code functions) | Swagger, JSON, XML, SQL, code | Breaks a single logical unit (one API endpoint, one function) across two chunks |
| Table-aware | Keeps table rows together, never splits a row mid-way | Any document with tables | Naive splitting can sever a row's columns across two chunks, making the row meaningless alone |
| Hierarchical | Preserves book → chapter → section → paragraph levels, queryable at any level | Long structured documents, books | Treats "broad question" and "narrow question" the same instead of letting you retrieve at the right granularity |
| Parent-child | Small chunks for matching (e.g. one "Authentication" section), but the larger parent ("Customer Search API") is what's returned | Enterprise API docs, anything where you need both precision and context | Small chunks match well but lack context; large chunks have context but match poorly — this gets both |
| Sliding window | Fixed-size window that slides forward with overlap, but tuned for sequential/temporal content | Logs, long conversations | Generic fixed-size chunking doesn't account for the chronological/sequential nature of logs — sliding window keeps recent context attached |
| Graph chunking | Extracts entities + relationships, represents the document as a graph rather than linear text chunks | Microservices docs, knowledge graphs | Linear chunking can't represent "Service A calls Service B which depends on Service C" — that's inherently graph-shaped, not paragraph-shaped |

## Decision guide (recap from the example in your notes)
For a "Customer API" doc with Authentication / Request / Response / Error Codes
sub-sections: **semantic or parent-child chunking**, not fixed-size — fixed-size
would happily cut "Authentication" away from its own error codes if they crossed
a 500-token boundary, even though they're clearly one logical unit a human reader
would never split.

## Where ChromaDB fits in this phase
This is the first phase where what you store actually matters downstream — the
chunk boundaries you choose here become the literal documents Chroma stores and
retrieves. The worksheet ingests the *same* source document chunked 4 different
ways into 4 separate Chroma collections, so you can directly compare retrieval
behavior caused purely by the chunking strategy, with everything else held constant.

## Teaser problem
> You used parent-child chunking for your API docs. A user asks "what's the auth
> header format for the Customer Search API?" Retrieval returns the *parent*
> chunk (the whole "Customer Search API" doc) every time, even though only the
> "Authentication" child section is relevant — burying the LLM in irrelevant
> Request/Response/Error text. What went wrong?

**Solution:** likely the *embedding* was computed on the parent chunk, not the
child — so similarity search is matching the broad parent representation instead
of the precise child one. The correct parent-child pattern: embed the **small
child chunks** for matching, but store a pointer to the parent and *return* the
parent only after a child chunk wins the similarity search. If you embedded the
parent text directly, you've collapsed parent-child back into plain fixed-size
chunking with extra bookkeeping. See the worksheet's parent-child section for the
fix implemented correctly.
