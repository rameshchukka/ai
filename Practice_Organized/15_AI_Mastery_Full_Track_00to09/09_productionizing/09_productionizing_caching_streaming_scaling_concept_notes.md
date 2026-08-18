# Module 9 — Productionizing

## 1. Caching
Identical (prompt, model, params) → identical-enough output for many use
cases. Caching saves cost and latency on repeated queries (common FAQ-style
questions, repeated agent sub-tasks). Key the cache on a hash of the full
request, not just the user-visible question — system prompt and params
changes should invalidate the cache.

## 2. Streaming
Returning tokens as they're generated rather than waiting for the full
response. Doesn't change total latency, but dramatically improves *perceived*
latency in a UI — users see progress immediately instead of staring at a
spinner. Every LangChain Runnable supports `.stream()` (Module 4); check
whether your in-house serving stack exposes a streaming endpoint at all.

## 3. Rate limiting & backpressure
Production systems need to handle "too many requests at once" gracefully —
either by queuing, by returning a clear rate-limit error the client can
retry, or by load-shedding low-priority requests first. This matters more
once you have *agents* in the loop, since one user request can fan out into
many model calls (one per tool-use step).

## 4. Fine-tuning vs RAG vs Prompt Engineering — decision framework
| | Prompt Engineering | RAG | Fine-tuning |
|---|---|---|---|
| Data needed | None/few examples | A document corpus | Hundreds-thousands of labeled examples |
| Cost to set up | Lowest | Medium (ingestion pipeline) | Highest (training infra/time) |
| Update cycle | Instant (edit the prompt) | Fast (re-ingest changed docs) | Slow (retrain) |
| Best for | Format/style/behavior changes | Knowledge that changes often or is too large for context | Deeply ingrained behavior/style changes prompting can't reliably achieve, or latency-sensitive cases where you can't afford a long prompt+context every call |
| Risk if misapplied | Limited — just doesn't work well | Garbage-in-garbage-out if retrieval is bad | Expensive failure if the data/approach was wrong |

**Default ordering for almost any new problem**: try prompt engineering first
→ add RAG if you need external/changing knowledge → consider fine-tuning only
if the first two demonstrably can't get you there (rare, in practice, for
most applied tasks).

## Teaser problem
> Your capstone agent works great in testing but the demo audience reports
> it "feels slow" even though your logs show the same total latency as
> testing. What's the most likely UX fix, and does it require touching the
> model at all?

**Solution:** add streaming (section 2) — the most likely issue isn't actual
latency, it's *perceived* latency from a blank screen during generation.
No model change needed, purely an output-handling change. See
the worksheet notebook in this folder for a before/after simulated comparison.
