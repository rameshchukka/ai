# LangChain — Composing LLM Applications — User Guide (Brain-Friendly)

> Plain-language walkthrough. No jargon dumps — just what this is, why it matters, and how to not get stuck.

## In One Paragraph

LangChain gives you reusable building blocks (prompts, chains, retrievers, memory, agents, tools) so you don't hand-roll the plumbing for every LLM app. It's most valuable once your app has more than one step.

## What You're About to Learn (and why it matters)

- PromptTemplate and output parsers
- Chains / LCEL (`|` pipe syntax) to compose steps
- Retrievers wired into a RAG chain end-to-end
- Conversation memory (buffer, summary) for multi-turn chat
- Tools + agents: letting the model decide which function to call
- Debugging a chain (verbose mode / tracing)

## Before You Start — Quick Mindset Tips

- 💡 Start without LangChain (plain API calls) to understand what it's abstracting — then adopt it once complexity grows.
- 💡 Keep chains small and composable; a 200-line single chain is a debugging nightmare.
- 💡 Give tools clear, narrow docstrings — the agent's tool-selection quality depends entirely on them.
- 💡 Use memory deliberately: full buffer memory grows unbounded token cost over a long chat.

## Things That Trip People Up

- 🚧 Over-engineering a single-prompt task into an agent (adds latency/cost/failure surface for no benefit).
- 🚧 Not capping agent iterations — a confused agent can loop indefinitely.
- 🚧 Version drift: LangChain's API changes fast; pin versions and read release notes.

## Where You'll Actually Use This

- Multi-step research assistant (search → summarize → answer)
- Customer support agent that can look up orders via a tool
- Document QA chatbot with memory across a session

## How to Study This Section (recommended flow)

1. **Skim first** — read through the notebook once without running code, just to get the shape of it.
2. **Run the worked examples** — actually execute every code cell; don't just read it.
3. **Attempt the TODOs yourself** before peeking at the solution — struggling a bit is where the learning happens.
4. **Explain it back** — in one or two sentences, explain the topic to yourself (or out loud) as if teaching someone else.
5. **Revisit tips above** if stuck; most beginner errors here are already listed.
