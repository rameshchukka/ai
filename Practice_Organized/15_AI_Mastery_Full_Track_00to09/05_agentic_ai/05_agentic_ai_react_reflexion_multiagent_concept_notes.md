# Module 5 — Agentic AI

## 1. Agent loop patterns
| Pattern | How it works | Strength | Weakness |
|---|---|---|---|
| ReAct | Reason → Act (tool call) → Observe → repeat | Simple, transparent trace | Can loop/flounder on hard multi-step problems |
| Plan-and-Execute | Plan all steps upfront, then execute each (re-plan if needed) | Better for tasks with a clear multi-step structure | Less adaptive if early steps reveal new info |
| Reflexion | After a final answer attempt, self-critique, and retry if flawed | Catches its own mistakes | Extra LLM calls = cost/latency |

## 2. Tool/function calling mechanics
The model is given tool *names + descriptions + parameter schemas*. It either:
(a) is natively trained to emit a structured tool-call object the serving
stack parses, or (b) is prompted to emit a JSON action object you parse
yourself (what you did in your earlier manual ReAct notebook). Either way,
the loop is: model proposes action → your code executes it → result fed back
as an "observation" → model continues.

## 3. Single-agent vs multi-agent orchestration
| Pattern | Structure | Use when |
|---|---|---|
| Single agent | One LLM, one tool set, one loop | Task fits in one coherent skillset/context |
| Supervisor | One "manager" agent delegates sub-tasks to specialist worker agents | Task naturally splits into distinct sub-skills (e.g. "research" + "code" + "write") |
| Hierarchical | Supervisors of supervisors | Very complex, large-scale multi-domain tasks |
| Swarm/peer-to-peer | Agents communicate directly without a central manager | Tasks needing decentralized negotiation/consensus |

**Practical bias:** start single-agent. Multi-agent adds real coordination
overhead (cost, latency, failure modes compound) — only split when one agent
demonstrably can't hold the task's full context/skillset.

## 4. Agent memory
| Type | What it holds | Analogy |
|---|---|---|
| Short-term | Current task's scratchpad/transcript | Working memory |
| Long-term | Persisted facts/preferences across sessions | Long-term memory |
| Episodic | Past full task traces, retrievable for similar future tasks | "I've solved something like this before" |

## 5. Guardrails for agents
- **Action allow-lists**: only let the agent call tools you've explicitly
  registered — never let it execute arbitrary code/shell commands it invents.
- **Max iteration caps**: prevent infinite loops (you already used
  `max_iterations`/`max_steps` in earlier notebooks).
- **Human-in-the-loop checkpoints**: require approval before high-stakes
  actions (sending an email, deleting data, spending money).
- **Injection awareness**: tool outputs/retrieved content can contain
  attacker-controlled text trying to redirect the agent — treat all tool
  output as untrusted data, not instructions (see Module 1's injection example).

## Teaser problem
> Your single ReAct agent keeps calling the same tool over and over with
> slightly different inputs, never reaching a final answer, until it hits
> `max_iterations`. What's likely wrong, and what are two different fixes?

**Solution:** likely the tool's observation isn't informative enough for the
model to know it succeeded/failed, or the task genuinely needs a plan the
ReAct pattern's "react one step at a time" style doesn't surface well. Fixes:
(1) make tool outputs more explicit/structured so success/failure is
unambiguous; (2) switch to Plan-and-Execute for this task so the model commits
to a full plan instead of re-deciding one step at a time. See the worksheet notebook in this folder
for both failure mode and fix reproduced live.
