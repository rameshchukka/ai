# Module 9 — Diagrams

## 1. Caching flow

```
   request (prompt, model, params)
              |
              v
        hash(request) -> cache key
              |
        ┌─────┴─────┐
        v           v
    cache HIT    cache MISS
        |           |
        v           v
   return cached  call model -> store in cache -> return
   (fast, free)    (slow, costs tokens)
```

## 2. Streaming vs non-streaming, perceived latency

```
 NON-STREAMING:
 [user sends request] ──────(blank screen, 3s)──────> [full answer appears]
                              ^ feels slow even if 3s is "fine" in absolute terms

 STREAMING:
 [user sends request] ─(0.2s)─> "The" "RAG" "pattern" "combines"...
                        ^ feels fast — progress visible almost immediately,
                          even though total time to finish is the same 3s
```

## 3. Rate limiting / backpressure

```
   incoming requests
        |  |  |  |  |  |
        v  v  v  v  v  v
   ┌─────────────────────┐
   │   Rate limiter        │
   └──────┬──────┬───────┘
          v      v
     within    over limit
     quota         |
        |          v
        v     ┌─────────┐
   process   │ queue OR  │
   normally  │ reject w/  │
              │ retry-after│
              └─────────┘
```

## 4. Fine-tune vs RAG vs Prompt Engineering — decision tree

```
              New problem to solve
                      |
        Can prompt engineering alone do it?
                      |
            ┌─────────┴─────────┐
           yes                  no
            |                    |
        Ship it.        Does it need external/
                         changing knowledge?
                                |
                      ┌─────────┴─────────┐
                     yes                  no
                      |                    |
                   Use RAG.      Is it a deep behavior/style
                                  change prompting truly can't
                                  achieve, AND you have enough
                                  labeled data?
                                          |
                                ┌─────────┴─────────┐
                               yes                  no
                                |                    |
                        Consider fine-tuning.   Re-examine the
                                                  prompt/RAG approach —
                                                  fine-tuning is rarely
                                                  the right first answer.
```
