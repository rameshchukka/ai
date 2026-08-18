# Capstone — Scoping & Shipping an AI Project — Developer Guide

> Technical reference for this section. Pair with the *User Guide (Brain-Friendly)* if you want the plain-language version first.

## Overview

The capstone is about the non-modeling skills that make an AI project actually ship: scoping, discovery questions, an honest MVP cut, and a clear architecture — not just writing code.

## What You Will Learn

- Running a discovery/requirements conversation with a stakeholder
- Writing a scoping document that separates must-have from nice-to-have
- Cutting an MVP: what's the smallest version that proves the idea?
- Sketching a system architecture (ingestion, processing, serving, monitoring)
- Identifying risks and unknowns early (data quality, latency, cost)

## Important Pointers / Tips

- **Tip:** Ask about failure cases and edge cases in discovery, not after building.
- **Tip:** Write the MVP cut before writing any code — it's a scoping tool, not an afterthought.
- **Tip:** Architecture diagrams should show data flow, not just boxes — trace one request through it.
- **Tip:** Budget for evaluation and guardrails work in your plan, not just the 'happy path' build.

## Common Pitfalls

- ⚠️ Scope creep from skipping a clear MVP cut.
- ⚠️ Underestimating integration/data-cleaning work vs. the 'interesting' modeling work.
- ⚠️ No plan for how you'll know the system is working after launch (monitoring/evals).

## Real-World Use Cases

- Scoping an internal AI assistant for a specific business function
- Turning a rough stakeholder ask into a concrete, buildable spec

## How to Use This Section

1. Read the relevant concept notes / notebooks already in this folder (if present).
2. Work through the `Real_World_Exercises` notebook — attempt each `# TODO` before checking the solution.
3. Revisit the tips/pitfalls above whenever something breaks — most bugs at this stage map to one of them.
