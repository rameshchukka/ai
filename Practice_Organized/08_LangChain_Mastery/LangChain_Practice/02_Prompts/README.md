# Prompts in LangChain: `PromptTemplate` vs `ChatPromptTemplate`

This folder demonstrates the two core ways LangChain builds prompts before sending
them to an LLM. Both classes do the same fundamental job — **turn variables into a
finished prompt** — but they produce different *shapes* of output, which is why each
fits a different kind of model and use case.

```
02_Prompts/
├── PromptTemplate/        → single-string prompts
└── ChatPromptTemplate/    → role-based, multi-message prompts
```

---

## 1. Why prompt templates exist at all

Hardcoding prompts as plain f-strings works for a demo, but breaks down fast:

- You can't reuse the same prompt with different inputs cleanly.
- There's no validation that you actually supplied every variable.
- You can't easily save/load prompts, version them, or chain them.
- Switching between "plain text" models and "chat" models means rewriting everything.

Prompt templates solve this. You declare the prompt **once** with placeholders like
`{context}` and `{question}`, then call `.invoke({...})` to fill them in. LangChain
handles substitution, validation, and producing the correct output type for the model.

---

## 2. `PromptTemplate` — a single text string

`PromptTemplate` produces **one flat string**. There are no roles (no "system" /
"user" / "assistant") — just text with placeholders.

From [PromptTemplate/prompt_template.py](PromptTemplate/prompt_template.py):

```python
from langchain_core.prompts import PromptTemplate

template_text = """
Use the following context to answer the question:

Context:
{context}

Question:
{question}

Answer:
"""

template = PromptTemplate(
    template=template_text,
    input_variables=['context', 'question'],
)

prompt = template.invoke({
    'context': "policy says an employee can take 5 days leave a year",
    'question': "How many days of leave can an employee take per year?"
})
```

The result is essentially one big string with the blanks filled in. That's it — no
conversation structure.

**Use `PromptTemplate` when:**
- The task is a single instruction → single answer (summarize, classify, translate,
  extract, "answer this question from this context").
- There is no back-and-forth conversation to maintain.
- You're filling a single text blob (e.g. a RAG "stuff the context in" prompt).
- You're working with a plain completion-style LLM.

---

## 3. `ChatPromptTemplate` — a list of role-tagged messages

Modern LLMs (Gemini, Claude, GPT, etc.) are **chat models**. They don't take one
string — they take a *list of messages*, each tagged with a role:

- `system` → who the model is / its rules
- `human` → the user's input
- `ai` → the model's previous replies

`ChatPromptTemplate` builds exactly that structure, with placeholders inside each
message.

From [ChatPromptTemplate/02_chatPromptTemplate_Dynamic.py](ChatPromptTemplate/02_chatPromptTemplate_Dynamic.py):

```python
from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate([
    ('system', 'You are a helpful {domain} expert'),
    ('human', 'Explain in simple terms, what is {topic}')
])

prompt = chat_template.invoke({
    'domain': 'astronomy',
    'topic': 'black holes'
})
```

The output is a list of messages, not a flat string — which is what chat models
actually expect.

> **Gotcha (already noted in the code):** use the tuple form `('system', '...{domain}...')`
> for dynamic prompts. Passing `SystemMessage('...{domain}...')` objects directly does
> **not** substitute variables — those are treated as pre-built, literal messages.

### Multi-turn conversations and memory

The real payoff of `ChatPromptTemplate` is handling **history**. With
`MessagesPlaceholder`, you reserve a slot where past turns get injected.

From [ChatPromptTemplate/03_ChatPromptTemp_messages_history.py](ChatPromptTemplate/03_ChatPromptTemp_messages_history.py):

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful customer support assistant."),
    MessagesPlaceholder(variable_name="chat_history"),  # past turns go here
    ("human", "{query}")
])

prompt = chat_template.invoke({
    "chat_history": chat_history,   # list of HumanMessage/AIMessage
    "query": user_input
})
```

This is what makes chatbots, agents, and tool-calling systems work — the model can
*see* the conversation so far.

**Use `ChatPromptTemplate` when:**
- You need a **system prompt** to set the model's persona/rules.
- The interaction is a **conversation** (multi-turn), not a one-shot.
- You need to preserve **chat history / memory** (`MessagesPlaceholder`).
- You're building **agents, RAG chat, tool calling, or conversational assistants**.
- You're using any modern chat model — which is almost always.

---

## 4. Raw messages vs. `ChatPromptTemplate`

You *can* build messages by hand, as in
[ChatPromptTemplate/00_chat_Messages.py](ChatPromptTemplate/00_chat_Messages.py):

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage(content='You are a helpful assistant'),
    HumanMessage(content='Tell me how to use trackpad in laptop')
]
result = model.invoke(messages)
messages.append(AIMessage(content=result.content))  # manually grow history
```

This works and is great for learning what's happening underneath. But there's **no
templating** — every value is hardcoded and you manage the list yourself.
`ChatPromptTemplate` is the reusable, variable-driven version of this same idea.

---

## 5. Side-by-side comparison

| | `PromptTemplate` | `ChatPromptTemplate` |
|---|---|---|
| **Output** | One text string | List of role-tagged messages |
| **Roles** | None | `system`, `human`, `ai` |
| **System prompt** | Not really (just text) | First-class |
| **Conversation history** | Awkward / manual | Built-in via `MessagesPlaceholder` |
| **Best model type** | Completion / single-shot | Chat models (Gemini, Claude, GPT…) |
| **Typical use** | Summarize, classify, single Q&A, RAG stuffing | Chatbots, agents, tool calling, multi-turn RAG |
| **Reusability** | High | High |

---

## 6. Quick decision guide

```
Is it a back-and-forth conversation, or do you need a system
prompt / chat history / agent / tool calling?
│
├── YES → ChatPromptTemplate
│
└── NO  → Is it a single instruction → single answer
          (summarize / classify / extract / one-shot Q&A)?
          │
          └── YES → PromptTemplate
```

**Rule of thumb:** In real agentic apps you'll reach for `ChatPromptTemplate`
almost every time, because system instructions + memory + roles are what agents,
RAG, and tool calling all depend on. Use `PromptTemplate` for the simpler,
stateless "fill one blank, get one answer" tasks.

---

## 7. The piece both share

Whichever you pick, the pattern is the same:

```
define template (with {placeholders})  →  .invoke({values})  →  model.invoke(prompt)
```

The only difference is what `.invoke()` hands to the model: a **string**
(`PromptTemplate`) or a **list of messages** (`ChatPromptTemplate`).
