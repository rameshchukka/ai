"""
integrated_triage.py
Week 15 - Part B, Step 5: Integrate with Week 14's triage system

Extends the Week 14 support-ticket-triage system so its "suggested_first_response"
is grounded in real policy documents via RAG, instead of relying on the model's
unaided (and potentially hallucinated) knowledge. Runs the same 5 sample tickets
both ways (without RAG, with RAG) so you can compare directly.

Run: python integrated_triage.py
Requires: you've already run `python ingest.py` at least once.
Writes results to before_after_comparison.md
"""

import json
from llm_client import call_llm
from generate import answer_question

# --- Ungrounded version (same idea as Week 14's triage system) --------------
TRIAGE_SYSTEM_NO_RAG = """You are a support ticket triage assistant for a SaaS company.
For each ticket, return ONLY valid JSON (no code fences, no explanation) matching:
{"urgency": "LOW|MEDIUM|HIGH", "product_area": string, "suggested_first_response": string}

Rules:
- Never promise a refund or a specific resolution timeline unless you are certain of policy.
- If you are unsure about a policy detail, the suggested_first_response should ask a
  clarifying question rather than state a policy as fact.
"""

# --- Grounded version: same shape, but response drafting is a 2-step process -
TRIAGE_SYSTEM_CLASSIFY_ONLY = """You are a support ticket triage assistant.
Classify the ticket. Return ONLY valid JSON (no code fences, no explanation) matching:
{"urgency": "LOW|MEDIUM|HIGH", "product_area": string, "policy_question": string}

The "policy_question" field should be the specific policy question that needs to be
answered in order to draft a helpful first response to this ticket (e.g. "what is the
refund window for an unopened item purchased 10 days ago?"). If no policy lookup is
needed, set policy_question to an empty string.
"""

SAMPLE_TICKETS = [
    "I bought a laptop stand 10 days ago and it arrived damaged. Can I get a refund "
    "or replacement?",
    "I'm in Germany and need this replacement part shipped express, is that possible?",
    "I want to add a 3-year extended warranty to the monitor I bought 2 months ago.",
    "This is my third time contacting you about the same billing issue, I want to "
    "speak to a manager.",
    "Can I get my subscription refunded, I signed up for the annual plan 20 days ago "
    "and changed my mind.",
]


def parse_json_safe(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[len("json"):].lstrip("\n")
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {"error": "invalid_json", "detail": str(e), "raw": raw_text}


def triage_without_rag(ticket: str) -> dict:
    raw = call_llm(TRIAGE_SYSTEM_NO_RAG, ticket, temperature=0.0)
    return parse_json_safe(raw)


def triage_with_rag(ticket: str) -> dict:
    # Step 1: classify + identify what policy question needs answering
    raw = call_llm(TRIAGE_SYSTEM_CLASSIFY_ONLY, ticket, temperature=0.0)
    classification = parse_json_safe(raw)

    # Step 2: if a policy lookup is needed, ground the response in real policy via RAG
    policy_question = classification.get("policy_question", "")
    if policy_question:
        rag_result = answer_question(policy_question)
        classification["suggested_first_response"] = rag_result["answer"]
        classification["grounded_in_sources"] = rag_result["sources_retrieved"]
    else:
        classification["suggested_first_response"] = (
            "Thanks for reaching out - could you share a bit more detail so we can help?"
        )
        classification["grounded_in_sources"] = []

    return classification


if __name__ == "__main__":
    lines = ["# Results: Before/After RAG Comparison\n"]

    for ticket in SAMPLE_TICKETS:
        no_rag = triage_without_rag(ticket)
        with_rag = triage_with_rag(ticket)

        print(f"\n=== Ticket: {ticket} ===")
        print("WITHOUT RAG:", json.dumps(no_rag, indent=2))
        print("WITH RAG:", json.dumps(with_rag, indent=2))

        lines.append(f"## Ticket\n\n> {ticket}\n")
        lines.append(f"**Without RAG:**\n\n```json\n{json.dumps(no_rag, indent=2)}\n```\n")
        lines.append(f"**With RAG:**\n\n```json\n{json.dumps(with_rag, indent=2)}\n```\n")

    lines.append(
        "## Reflection\n\n"
        "_TODO: Compare the 'suggested_first_response' field across both versions "
        "for each ticket. Where did the ungrounded version hedge vaguely or risk "
        "an incorrect policy claim, and where did the RAG-grounded version give a "
        "specific, citable, correct answer? Write 3 sentences on what changed and "
        "why it matters for customer trust._\n"
    )

    with open("before_after_comparison.md", "w") as f:
        f.write("\n".join(lines))
    print("\nResults written to before_after_comparison.md")
