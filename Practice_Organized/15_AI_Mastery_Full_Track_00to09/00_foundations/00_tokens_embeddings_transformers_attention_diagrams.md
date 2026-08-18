# Module 0 — Diagrams

## 1. End-to-end pipeline (every LLM call)

```
"What is RAG?"
      |
      v
 [Tokenizer]  ->  ["What", " is", " RAG", "?"]
      |
      v
 [Token IDs]  ->  [4023, 318, 26516, 30]
      |
      v
 [Embedding lookup table]  ->  4 vectors (e.g. dim=4096 each)
      |
      v
 +-------------------------------------+
 |  Transformer block x N              |
 |   ┌─────────────────────────┐       |
 |   │ Self-Attention (Q,K,V)  │       |   <- repeated N times
 |   ├─────────────────────────┤       |      (N = "layers", e.g. 32, 80)
 |   │ Feed-Forward Network    │       |
 |   └─────────────────────────┘       |
 +-------------------------------------+
      |
      v
 [Output logits]  -> probability over entire vocabulary
      |
      v
 [Sampling: temperature/top-p/top-k]  -> pick next token
      |
      v
 append token, repeat until stop condition
```

## 2. Type hierarchy: Transformer architectures

```
                    Transformer
                        |
        ┌───────────────┼───────────────┐
        |               |               |
   Encoder-only    Decoder-only    Encoder-Decoder
   (bidirectional)  (causal)       (both)
        |               |               |
     BERT-family    GPT/Llama/Qwen   T5 / original
   Jina-embeddings   Mistral/Devstral  Transformer
   (your MODEL_JINA) (your chat models)  (translation,
                                          seq2seq tasks)
```

## 3. Self-attention, one token's view

```
   Token: "RAG"
        |
        v
   Query vector  ──┐
                    │  dot product with every
   Key vectors ─────┤  other token's Key
   (every token)     │
                    v
            attention scores
                    |
                 softmax
                    |
                    v
       weighted sum of Value vectors
                    |
                    v
        updated representation of "RAG"
        (now context-aware: knows it's
         near "What" and "is")
```

## 4. Why context window is quadratic (informal)

```
seq_len = 4   ->  4 x 4  = 16 attention pairs to compute
seq_len = 8   ->  8 x 8  = 64 attention pairs
seq_len = 16  -> 16 x 16 = 256 attention pairs

Doubling input length quadruples attention compute.
This is the root cause of context-window limits and
the core motivation for RAG (retrieve a small relevant
slice instead of feeding everything).
```
