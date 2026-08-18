# Agents & Orchestration — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

An 'agent' is an LLM that can decide which action/tool to take next, observe the result, and iterate — instead of just producing one-shot text. Orchestration is about coordinating multiple steps/agents reliably.

## What You Will Learn

- The ReAct pattern: Reason → Act → Observe → repeat
- Defining tools with clear inputs/outputs the model can call
- Approval/human-in-the-loop steps for risky actions
- Chunking and retrieval as tools inside an agent loop
- Basic multi-agent orchestration (a planner + specialist workers)

## Important Pointers / Tips

- **Tip:** Give the agent a maximum step count and a fallback message — never let it run unbounded.
- **Tip:** Make tool errors return a clear string the model can read and react to, not a raw stack trace.
- **Tip:** Log every reasoning/action/observation step during development — it's your only debugging window.
- **Tip:** Prefer the smallest number of tools/agents that solves the task; more moving parts = more failure modes.

## Common Pitfalls

- ⚠️ Ambiguous tool descriptions causing the wrong tool to be picked.
- ⚠️ No approval gate before an irreversible action (sending an email, making a purchase).
- ⚠️ Treating agent output as ground truth without a verification step.

## Real-World Use Cases

- An eligibility/approval workflow that gathers data via tools then asks a human to confirm
- A research agent that searches, retrieves, and drafts a report
- A multi-agent pipeline: planner agent delegates to specialist agents

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
