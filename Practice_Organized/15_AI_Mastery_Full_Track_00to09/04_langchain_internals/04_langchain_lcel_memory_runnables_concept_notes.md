# Module 4 — LangChain / Framework Internals

## 1. Core abstractions
- **LLM**: string in, string out (your `InHouseLLM`).
- **ChatModel**: message list in, message out — distinguishes system/human/AI
  roles natively. Most modern model integrations are ChatModels, not LLMs.
- **PromptTemplate / ChatPromptTemplate**: parameterized prompt with `{variables}`.
- **OutputParser**: turns raw model text into a structured Python object
  (`StrOutputParser`, `JsonOutputParser`, `PydanticOutputParser`).
- **Runnable**: the universal interface — anything with `.invoke()`. Prompts,
  models, parsers, and your own functions can all be Runnables, which is why
  they compose with `|`.

## 2. Chains (legacy) vs Runnables/LCEL (current)
| | Chains (e.g. `LLMChain`, `RetrievalQA`) | LCEL (`prompt | llm | parser`) |
|---|---|---|
| Style | Class-based, pre-built chain types | Declarative, compose with `|` |
| Flexibility | Limited to what the chain class supports | Fully composable — swap any piece |
| Streaming/async | Inconsistent across chain types | Built-in, consistent across all Runnables |
| Current guidance | Being phased out in favor of LCEL | The recommended approach going forward |

**Practical note:** you used `RetrievalQA.from_chain_type(...)` in the earlier
RAG project — that's the legacy chain style. Worth re-implementing it as an
LCEL pipeline once you're comfortable with this module; see the worksheet.

## 3. Memory types
| Type | Stores | Use when |
|---|---|---|
| Buffer | Full raw conversation history | Short conversations, simplicity |
| Summary | LLM-generated running summary instead of full history | Long conversations, want to save tokens |
| Entity | Tracks facts about specific named entities mentioned | Conversations referencing people/things repeatedly |
| Vector-backed | Stores past turns in a vector store, retrieves relevant ones | Very long-running assistants, need selective recall |

## 4. LangGraph — state machines for agents
LCEL composes *linear* (or simple branching) pipelines. Real agents often need
**cycles** (loop until done) and **explicit state** (track multiple variables
across steps) — that's what LangGraph adds: a graph of nodes (each a Runnable
or function) and edges (including conditional ones), with a shared state
object passed between them. This is the more powerful backbone Module 5's
agent loops are usually built on in production, beyond the basic
`AgentExecutor` you used earlier.

## Teaser problem
> You built a chain with `RetrievalQA.from_chain_type(...)`. Your product
> manager wants streaming output (tokens appearing as they generate) for the
> UI. The legacy chain doesn't support it well. What's the fix?

**Solution:** rebuild the same logic as an LCEL pipeline
(`retriever | prompt | llm | StrOutputParser()`) and call `.stream()` instead
of `.invoke()` — every Runnable supports streaming consistently, which is
exactly the gap LCEL was built to close. See the worksheet notebook in this folder.
