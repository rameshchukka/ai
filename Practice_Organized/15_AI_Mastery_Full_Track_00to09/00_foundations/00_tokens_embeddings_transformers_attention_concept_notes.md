# Module 0 — Foundations: Tokens, Embeddings, Transformers, Attention

## 1. The pipeline every LLM call goes through
Text never enters a model as text. It goes: **raw text → tokens → token IDs →
embeddings → transformer layers → output logits → sampled token → repeat.**

- **Tokenization**: splits text into sub-word units (not always whole words).
  `"unbelievable"` might become `["un", "believ", "able"]`. This is why token
  count ≠ word count — budget context windows in tokens, not words.
- **Embedding (input)**: each token ID maps to a learned vector (e.g. 4096-dim).
  This is a *lookup table*, different from the sentence-embedding models you
  use for RAG (those produce one vector per whole text, via pooling).
- **Transformer layers**: stacked blocks of self-attention + feed-forward,
  refining each token's vector using context from other tokens.
- **Output**: the final layer produces a probability distribution over the
  vocabulary for "what token comes next." Sampling (Module 1) picks one.

## 2. Self-attention, conceptually
Each token asks: "which other tokens should I pay attention to, to understand
my role in this sentence?" It does this via three learned projections:
- **Query (Q)**: what this token is looking for
- **Key (K)**: what each token offers
- **Value (V)**: the actual content each token contributes if attended to

Attention score = how well a token's Query matches another token's Key →
softmax → weighted sum of Values. This happens for every token, in parallel,
across multiple "heads" (multi-head attention) that each learn different
relationships (e.g., one head tracks grammar, another tracks long-range topic).

## 3. Encoder vs Decoder vs Decoder-only
| Architecture | Attention direction | Good at | Examples |
|---|---|---|---|
| Encoder-only | Bidirectional (sees full input at once) | Understanding/classification, embeddings | BERT, Jina embeddings |
| Decoder-only | Causal (each token only sees earlier tokens) | Generation, chat, completion | GPT, Llama, Qwen, Mistral |
| Encoder-Decoder | Encoder bidirectional, decoder causal + cross-attends to encoder | Translation, structured seq2seq | T5, original Transformer |

**Practical takeaway:** every chat model in your in-house stack (Qwen3, Mistral,
Llama, Devstral) is decoder-only. Your embedding model (Jina) is encoder-style
under the hood — that's *why* it's a separate model rather than something you
ask Qwen3 to do.

## 4. Why context window size is a hard limit, not a guideline
Attention cost grows quadratically with sequence length (every token attends
to every other token). This is *why* context windows are bounded and why
RAG exists at all: instead of stuffing your whole knowledge base into context,
you retrieve only the relevant slice.

## See also
- the diagrams file in this folder in this folder for the ASCII flow/hierarchy diagrams
- the worksheet notebook in this folder for hands-on tokenization + manual attention computation
