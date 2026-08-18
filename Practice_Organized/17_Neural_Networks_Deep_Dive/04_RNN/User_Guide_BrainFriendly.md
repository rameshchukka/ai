# Recurrent Neural Networks (RNNs) & Sequence Models — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

RNNs process sequences step by step, carrying a hidden state forward so the network has 'memory' of earlier elements — the classical approach to text, time series, and other ordered data (now often superseded by Transformers for text, but still foundational and used for many time-series tasks).

## What You're About to Learn (and why it matters)

- The recurrence relation: hidden state updates as the sequence is processed
- Vanishing gradients over long sequences, and why LSTM/GRU were introduced
- LSTM/GRU gating intuition (what to keep, forget, output)
- Sequence-to-one vs. sequence-to-sequence architectures
- Where Transformers (attention) replaced RNNs, and where RNNs are still used

## Before You Start — Quick Mindset Tips

- 💡 For long sequences, prefer LSTM/GRU over a vanilla RNN — they handle long-range dependencies far better.
- 💡 Pad/truncate sequences to a consistent length per batch, and mask padding in the loss.
- 💡 For most modern NLP tasks, a pretrained Transformer will outperform an RNN you train from scratch — RNNs remain strong for smaller time-series problems.

## Things That Trip People Up

- 🚧 Not masking padded timesteps, letting the model learn from meaningless padding.
- 🚧 Expecting a vanilla RNN to remember information from very early in a long sequence.

## Where You'll Actually Use This

- Time-series forecasting (demand, sensor data)
- Sequence tagging tasks and historically, language modeling/translation (now largely Transformer-based)

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
