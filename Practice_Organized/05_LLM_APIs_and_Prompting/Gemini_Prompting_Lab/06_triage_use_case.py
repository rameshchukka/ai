"""
06_triage_use_case.py
Week 14 - Real-World Use Case: Support Ticket Triage System

Classifies urgency, extracts structured metadata, and drafts a suggested
first-response for incoming support tickets - the capstone exercise tying
together few-shot prompting, structured output, and hallucination-avoidance
from this week's tutorial.

Run: python 06_triage_use_case.py
Writes results to results_triage.md
"""

import json
from llm_client import call_llm
from importlib import import_module

# Reuse the defensive parser from Exercise 4
_structured = import_module("04_structured_output")
parse_llm_json = _structured.parse_llm_json

TRIAGE_SYSTEM = """You are a support ticket triage assistant for a SaaS company.
For each ticket, return ONLY valid JSON (no code fences, no explanation) matching:
{"urgency": "LOW|MEDIUM|HIGH", "customer_name": string, "product_area": string,
 "sentiment": "positive|neutral|negative", "suggested_first_response": string}

Rules:
- Never promise a refund or a specific resolution timeline.
- If you are unsure about a policy detail, the suggested_first_response should ask
  a clarifying question rather than state a policy as fact.
- Never invent a customer name if none is given - use an empty string.
"""

# TODO: write 5 realistic-sounding fictional tickets of your own (vary tone,
# urgency, completeness). The 3 below are a working example.
SAMPLE_TICKETS = [
    "Hi, this is Priya. I've been charged twice this month and I need this "
    "fixed ASAP, this is really frustrating.",
    "hey when is dark mode coming out lol",
    "URGENT - production integration down since this morning, losing "
    "customers, please call me. - James, Acme Corp",
]


def run_triage():
    lines = ["# Results: Support Ticket Triage System\n"]

    for ticket in SAMPLE_TICKETS:
        raw = call_llm(TRIAGE_SYSTEM, ticket, temperature=0.0)
        parsed = parse_llm_json(raw)

        print("Ticket:", ticket[:70], "...")
        print("Parsed:", json.dumps(parsed, indent=2))
        print()

        lines.append(f"## Ticket\n\n> {ticket}\n")
        lines.append(f"**Parsed result:**\n\n```json\n{json.dumps(parsed, indent=2)}\n```\n")

    lines.append(
        "## CTO Briefing Paragraph\n\n"
        "_TODO: Write the paragraph described in the tutorial's real-world use "
        "case - as if answering the customer's CTO's question: 'How do we know "
        "this system won't just make things up?' Reference the constraints in "
        "TRIAGE_SYSTEM above (no invented promises, ask-a-clarifying-question "
        "fallback) and note that full grounding via RAG arrives in Week 15._\n"
    )

    with open("results_triage.md", "w") as f:
        f.write("\n".join(lines))
    print("Results written to results_triage.md")


if __name__ == "__main__":
    run_triage()
