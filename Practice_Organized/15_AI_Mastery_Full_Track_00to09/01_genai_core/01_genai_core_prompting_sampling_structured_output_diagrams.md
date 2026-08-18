# Module 1 — Diagrams

## 1. Model family decision tree (your in-house stack)

```
                         What's the task?
                                |
        ┌───────────────┬──────┴──────┬───────────────┬───────────────┐
        v               v             v               v               v
   "chat/RAG       "needs hard    "writing/     "understand an   "need a
    answer"         reasoning"    debugging      image/chart"     vector for
        |               |         code"              |            search"
        v               v             |               v               v
  MODEL_QWEN3_14B  MODEL_QWEN3_30B     v          MODEL_QWEN2_5_   MODEL_JINA
  (default)        (multi-step    MODEL_DEVSTRAL   VL_7B
                    agent planning)

        "need to evaluate / score another model's answer?"
                                |
                                v
                         MODEL_LLAMA (70B)
```

## 2. Sampling parameter effect (informal)

```
 logits:  [cat: 5.0, dog: 4.8, fish: 1.0, ...]

 temperature -> 0.1   "cat" picked ~99% of the time   (deterministic)
 temperature -> 1.0   "cat" ~55%, "dog" ~40%, ...      (balanced)
 temperature -> 2.0   flatter distribution, "fish"     (chaotic/creative)
                       now has a real shot

 top-p = 0.9   -> keep adding tokens by probability until
                  cumulative mass hits 90%, sample only from those
 top-k = 5     -> only ever consider the 5 highest-probability tokens
```

## 3. Prompt structure for reliable structured output

```
 ┌─────────────────────────────────────────┐
 │ SYSTEM PROMPT                            │
 │  - role/persona                          │
 │  - OUTPUT SCHEMA (put it here, not below)│  <- highest-weight instructions
 │  - "ONLY valid JSON, no fences"          │
 └─────────────────────────────────────────┘
 ┌─────────────────────────────────────────┐
 │ USER PROMPT                              │
 │  - the actual content/question           │
 │  - (optional) one example output         │  <- few-shot anchor
 └─────────────────────────────────────────┘
                  |
                  v
         model response (raw string)
                  |
                  v
     strip fences -> json.loads() -> validate
```
