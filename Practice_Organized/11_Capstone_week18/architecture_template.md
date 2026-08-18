# Architecture Sketch

*Sketch the flow before writing any code. ASCII/markdown diagram is fine — the point is
forcing yourself to think through the pipeline end to end before Month 6's build sprints.*

## High-Level Flow

```
[Data Sources]  -->  [Ingestion / RAG Layer]  -->  [Agent / Tool Layer]  -->  [Eval / Guardrail Layer]  -->  [Output / Integration Point]
```

Fill in each box with what's actually going in it for YOUR capstone:

### Data Sources
*What data does this system need access to? Where does it live today?*
- _TODO_

### Ingestion / RAG Layer
*What gets chunked and embedded? What's the knowledge base? (Reuse Lab 2's pattern if
applicable.)*
- _TODO_

### Agent / Tool Layer
*What tools does the agent need? What actions can it take autonomously vs. what needs human
approval? (Reuse Lab 3's pattern if applicable.)*
- _TODO_

### Eval / Guardrail Layer
*What does "working correctly" mean for this system, measurably? What guardrails are
non-negotiable before this touches a real customer? (Reuse Lab 4's pattern if applicable.)*
- _TODO_

### Output / Integration Point
*Where does the result actually go? A dashboard? An API another system calls? A Slack
message? Be concrete.*
- _TODO_

## Open Technical Questions
*What don't you know yet that you'll need to figure out during the build sprints?*
- _TODO_
