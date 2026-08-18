# Module 3 — RAG (Retrieval-Augmented Generation)

## 1. The core architecture
Retriever + Generator. The retriever's job is to narrow a huge corpus down to
a handful of relevant chunks; the generator's job is to turn those chunks
plus the question into a grounded answer. Everything else (chunking strategy,
hybrid search, reranking, query rewriting) exists to make the retriever's
output better, because **a generator can't recover from bad retrieval** — it
will confidently answer from whatever it's given, right or wrong.

## 2. Chunking strategies
| Strategy | How it splits | Best for | Risk |
|---|---|---|---|
| Fixed-size | Every N characters/tokens | Quick prototyping | Cuts sentences/ideas mid-thought |
| Recursive | Tries paragraph → sentence → word boundaries, in order | General prose | Still somewhat arbitrary boundaries |
| Structural | Splits on document structure (headers, rows, Q&A pairs) | Tables, FAQs, markdown docs | Needs structure-aware parsing per source type |
| Semantic | Splits where embedding similarity between adjacent sentences drops | Long-form prose without clear structure | Slower (needs embeddings during ingestion) |
| Parent-child | Small chunks for retrieval matching, but return the larger parent chunk for context | Balances precise matching with enough context for generation | More bookkeeping (track parent-child mapping) |

## 3. Retrieval modes
- **Dense (vector)**: semantic similarity via embeddings. Misses exact-match terms (IDs, model names).
- **Sparse (BM25/keyword)**: exact term matching, weighted by term rarity. Misses paraphrases/synonyms.
- **Hybrid**: combine both rankings (commonly via weighted score fusion or
  Reciprocal Rank Fusion). Standard in production RAG — covers both failure modes.
- **Metadata filtering**: narrow the candidate set by structured fields
  (date, owner, doc type) *before or alongside* similarity search.

## 4. Reranking
A cross-encoder (Module 2) or an LLM-as-reranker re-scores the top-k from
initial retrieval. Use when initial retrieval is cheap-but-noisy and you can
afford a slower, more accurate second pass over a small candidate set.

## 5. Generation patterns
| Pattern | How | Use when |
|---|---|---|
| Stuff | All retrieved chunks go into one prompt | Chunks fit comfortably in context |
| Map-reduce | Summarize/answer per chunk, then combine | Too many chunks for one context window |
| Refine | Process chunks sequentially, refining the answer each time | Need the latest chunk to be able to revise prior conclusions |

## 6. Advanced RAG techniques
- **Query rewriting**: ask the LLM to reformulate the user's question into a
  better search query before embedding it (fixes vague/colloquial queries).
- **HyDE (Hypothetical Document Embeddings)**: ask the LLM to *hallucinate* a
  plausible answer first, embed THAT, and search with it — often matches
  real documents better than embedding the raw question.
- **Multi-query**: generate several rephrasings of the question, retrieve for
  each, merge/deduplicate results — covers more of the relevant space.
- **Graph RAG**: build a knowledge graph from documents (entities + relations),
  retrieve via graph traversal in addition to/instead of vector similarity —
  better for multi-hop questions spanning several documents.

## 7. Evaluation
| Metric | Question it answers |
|---|---|
| Faithfulness | Does the answer only use facts present in the retrieved context? |
| Answer relevance | Does the answer actually address the question? |
| Context precision | Of the retrieved chunks, how many were actually relevant? |
| Context recall | Of all relevant chunks in the corpus, how many were retrieved? |

These four (the RAGAS-style framework) separate retrieval problems from
generation problems — critical for debugging *which half* of RAG is failing.

## Teaser problem
> Your RAG answers are fluent and confident but factually wrong — the model
> seems to be "filling in" with general knowledge instead of the retrieved
> context. Where do you look first?

**Solution:** check context precision/recall first — if the retriever isn't
returning the actually-relevant chunk, the generator has nothing grounded to
work from and falls back on its parametric knowledge. Only after confirming
retrieval is solid should you tighten the generation prompt ("answer ONLY
using the context, say 'I don't know' if it's not there"). See
the worksheet notebook in this folder for a reproduction using a deliberately bad retriever vs a
good one on the same question.
