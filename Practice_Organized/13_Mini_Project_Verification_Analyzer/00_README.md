# Kibana Log Verification Engine — Build Playbook (Phase 1 + Phase 2)

This package is the planning layer for building the two-phase system: **Phase 1** (Log
Verification Engine, `Requirment_Document.txt`) and **Phase 2** (Distributed Transaction
Statistics & Performance Analyzer, `Log_Statistics.txt`). 25 milestones total — M0–M12 for Phase
1, M13–M24 for Phase 2 — designed to be handed to a coding agent (Claude Code or similar, with
file/tool access) one milestone at a time, so the build survives across many short, token-limited
sessions instead of needing one giant context.

Phase 2 consumes Phase 1's output and nothing else — it reads the verified `LogRepository`
produced by Phase 1's M12 and performs no parsing, timestamp handling, or rule logic of its own.
**Phase 2 milestones should not be started until Phase 1 (M0–M12) is fully Complete.**

## The core problem this solves

A coding agent in a single session only has so much context. If you paste the whole 14-section
spec and say "build it," the agent either runs out of room, loses track of earlier decisions, or
quietly reinterprets things differently between sessions. The fix is the same one humans use on
real engineering teams: **write down the decisions once, write down progress after every step,
and only hand the agent what it needs for the step it's on.**

## The artifact set

| File | Answers | Changes how often |
|---|---|---|
| `Requirment_Document.txt` → rename `REQUIREMENTS.md` | **What** to build, Phase 1 (source of truth) | Never (it's the spec) |
| `Log_Statistics.txt` → rename `REQUIREMENTS_PHASE2.md` | **What** to build, Phase 2 (source of truth) | Never (it's the spec) |
| `01_ARCHITECTURE.md` | **How** it's built — stack, patterns, structure | Rarely — amend via ADR if a milestone forces a real change. **Currently Phase 1 only** — Phase 2's working decisions live as informal "Design notes" inside `03_MILESTONES.md` until formalized here. |
| `02_UI_DESIGN.md` | What each screen looks like and does, both phases | Rarely |
| `03_MILESTONES.md` | **When** — small, ordered, independently-verifiable slices, both phases | Rarely — mark items done, don't rewrite scope mid-stream |
| `04_PROJECT_STATUS.md` | Where things stand **right now**, both phases | After every single milestone — this is the agent's memory |
| `05_PROMPTS.md` | The exact instruction to paste in for each milestone, both phases | Used once per milestone |

## The loop (repeat once per milestone)

1. Start a **fresh** agent session (don't rely on chat history carrying state).
2. Copy the prompt for the next milestone from `05_PROMPTS.md` and paste it in.
3. The agent reads `04_PROJECT_STATUS.md` first, then only the spec/architecture/UI sections that
   prompt points it to — not the entire document set, not prior transcripts.
4. The agent implements **only** that milestone, writes tests, and re-runs the **full** test suite
   to confirm nothing earlier broke.
5. The agent rewrites `04_PROJECT_STATUS.md` before stopping — that's the save file.
6. You skim the diff, commit to git, and move to the next prompt.

If a session runs out of room mid-milestone, that's fine — the next session re-reads
`PROJECT_STATUS.md`'s "Context for Next Agent Session" note and picks up exactly where it left
off, because that note is written in plain language, not assumed from memory.

## Why this is the "proficient" way

- **Context-window discipline**: each session loads a status file + 1–2 spec sections, not the
  whole history. This is the main lever for working around token limits.
- **External memory**: progress lives in a file, not in a conversation, so it survives across
  sessions, context resets, or even switching to a different agent entirely.
- **Small, traceable slices**: every milestone maps to one numbered section of the requirements
  doc. If something's wrong, you know exactly which milestone to revisit.
- **Decide architecture once**: the agent isn't re-inventing the field-mapping approach or the
  rule-engine pattern every milestone — it's already decided and written down, so output stays
  consistent session to session.
- **Regression checked every time**: "verify what's built so far still works" is baked into every
  prompt, not left to chance.

## Ground rules for every agent session (also embedded in each prompt)

- Never implement ahead of the current milestone, even if the next feature seems trivial to add
  while you're in there.
- Never silently modify a previously-completed milestone's code — if a regression forces a
  change, log it in `PROJECT_STATUS.md` under "Deviations."
- Always run the full test suite, not just tests for the new code.
- Always end the session by updating `PROJECT_STATUS.md` and stating plainly: *"Milestone X
  complete"* or *"Milestone X blocked because Y."*

## Suggested repo layout

```
kibana-log-verifier/
├── REQUIREMENTS.md          (renamed from Requirment_Document.txt — Phase 1)
├── REQUIREMENTS_PHASE2.md   (renamed from Log_Statistics.txt — Phase 2)
├── ARCHITECTURE.md
├── UI_DESIGN.md
├── MILESTONES.md
├── PROJECT_STATUS.md
├── app/
│   ├── __init__.py
│   ├── config/
│   ├── core/
│   ├── blueprints/
│   ├── templates/
│   └── static/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── run.py
└── requirements.txt
```

## Getting started

1. Drop all 7 files (this README + the 5 docs + both requirements docs) into the repo root.
2. Rename `Requirment_Document.txt` → `REQUIREMENTS.md` and `Log_Statistics.txt` →
   `REQUIREMENTS_PHASE2.md` (the prompts assume these names; adjust if you'd rather keep the
   original filenames).
3. `git init`, commit the planning docs as commit zero.
4. Open `05_PROMPTS.md`, copy the **M0** prompt, paste it into your agent.
5. Work through M0–M12 (Phase 1) before touching any M13+ prompt — Phase 2 depends on Phase 1's
   finished, documented repository interface.

## A note on this being a living plan

You mentioned you'll revisit/override this planning set once Phase 1 is actually built — that's
expected and reasonable. Phase 2's milestones here are necessarily written against the *spec*,
not against Phase 1's real implementation details, so once M12 closes out and
`PHASE2_INTERFACE.md` exists, it's worth a quick pass to confirm M13–M24 still line up with what
Phase 1 actually shipped (method names, field names, etc.) before running the M13 prompt.
