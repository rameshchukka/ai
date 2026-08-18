# Module 5 — Diagrams

## 1. ReAct loop

```
   ┌─────────────────────────────────────────┐
   │  Question                                │
   └───────────────────┬───────────────────────┘
                        v
              ┌──────────────────┐
        ┌────>│  Thought (reason) │
        │     └─────────┬────────┘
        │               v
        │     ┌──────────────────┐
        │     │  Action (tool call)│
        │     └─────────┬────────┘
        │               v
        │     ┌──────────────────┐
        │     │  Observation       │
        │     └─────────┬────────┘
        │               v
        │        final answer? ── no ──┘ (loop, up to max_iterations)
        │               |
        │              yes
        │               v
        └────>   Final Answer
```

## 2. Plan-and-Execute

```
  Question
     |
     v
 ┌────────────────────────────┐
 │ Planner LLM: produce full   │
 │ ordered list of steps        │
 └──────────────┬──────────────┘
                v
       [Step 1, Step 2, Step 3, ...]
                |
                v
     ┌─────────────────────┐
     │ Executor: run Step 1  │──> result
     │ Executor: run Step 2  │──> result   (can re-plan here if a
     │ Executor: run Step 3  │──> result    step's result invalidates
     └─────────────────────┘                the remaining plan)
                |
                v
          Final Answer
```

## 3. Multi-agent supervisor pattern

```
                    ┌───────────────┐
                    │  Supervisor    │
                    │  agent          │
                    └───┬───┬───┬────┘
              delegates  |   |   |  delegates
                    ┌────┘   |   └────┐
                    v        v        v
            ┌──────────┐┌──────────┐┌──────────┐
            │ Research  ││  Coding   ││  Writing  │
            │ agent     ││  agent    ││  agent    │
            └──────────┘└──────────┘└──────────┘
                    |        |        |
                    └────────┼────────┘
                             v
                  Supervisor merges results
                  into final response
```

## 4. Agent memory hierarchy

```
                  Agent Memory
                        |
        ┌───────────────┼───────────────┐
        v               v               v
   Short-term       Long-term         Episodic
   (this task's     (persisted facts  (past full task
    scratchpad)      across sessions)  traces, retrieved
        |               |              for similar future
   cleared after    survives across    tasks via vector
   task ends         sessions          search)
```
