"""
guardrails.py
Week 17 - Step 6: Guardrails

Two guardrails that live in CODE, not just in the prompt - the point being
that a guardrail the model can be talked out of isn't a guardrail:
  1. Input guardrail: heuristic detection of likely prompt-injection patterns
     in incoming ticket text, flagged BEFORE the ticket ever reaches the model.
  2. Output guardrail: schema validation that blocks a malformed response
     from ever reaching a (simulated) downstream system.

Run: python guardrails.py
Tests both guardrails against the 5 adversarial cases in eval_set.json.
"""

import re
from triage_system import classify_ticket, is_schema_valid
from eval_runner import load_eval_set

# Heuristic patterns commonly seen in prompt-injection attempts. This is
# intentionally simple (real production systems use more robust detection,
# often a dedicated classifier) - the point here is the ARCHITECTURE pattern
# (guardrail lives in code, runs before/after the model, blocks regardless
# of what the model itself decides) not building a perfect detector.
INJECTION_PATTERNS = [
    r"ignore (all |your )?(previous |prior |above )?instructions",
    r"disregard (your |the )?(instructions|prompt)",
    r"system\s*:",
    r"you are now",
    r"admin (mode|debug)",
    r"reveal your (system )?prompt",
    r"forget everything",
    r"drop table",
]


def input_guardrail(ticket_text: str) -> dict:
    """Returns {"flagged": bool, "matched_patterns": [...]} - does NOT block
    the ticket from being processed (a real system might still want to
    triage it normally, per TRIAGE_SYSTEM's own instruction to treat
    injection attempts as the issue to report) but flags it for downstream
    handling/logging regardless of what the model decides to do with it."""
    matched = []
    lowered = ticket_text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lowered):
            matched.append(pattern)
    return {"flagged": len(matched) > 0, "matched_patterns": matched}


def output_guardrail(parsed_response: dict) -> dict:
    """Blocks a malformed response from reaching a downstream system. This
    reuses triage_system.is_schema_valid() - the SAME check used in the eval
    runner, on purpose: an eval and a guardrail are the same check, just
    applied at different times (eval = before you ship, guardrail = every
    single production request)."""
    valid = is_schema_valid(parsed_response)
    return {
        "allowed_downstream": valid,
        "reason": "Schema valid" if valid else "BLOCKED - malformed or incomplete response",
    }


if __name__ == "__main__":
    eval_set = load_eval_set()
    adversarial_cases = [c for c in eval_set if c["adversarial"]]

    print(f"Testing guardrails against {len(adversarial_cases)} adversarial cases\n")

    for case in adversarial_cases:
        print(f"--- {case['id']} ---")
        print(f"Ticket: {case['ticket'][:80]}...")

        in_result = input_guardrail(case["ticket"])
        print(f"Input guardrail: flagged={in_result['flagged']} "
              f"(matched: {in_result['matched_patterns']})")

        parsed = classify_ticket(case["ticket"])
        out_result = output_guardrail(parsed)
        print(f"Output guardrail: allowed_downstream={out_result['allowed_downstream']} "
              f"({out_result['reason']})")
        print()

    flagged_count = sum(1 for c in adversarial_cases if input_guardrail(c["ticket"])["flagged"])
    print(f"Summary: {flagged_count}/{len(adversarial_cases)} adversarial cases flagged by input guardrail.")
    print(
        "\nTODO: For any adversarial case NOT flagged, either it's a legitimately subtle "
        "case your heuristic patterns don't cover (add a pattern), or it's a reminder "
        "that regex-based detection has real limits - note this in your reliability report."
    )
