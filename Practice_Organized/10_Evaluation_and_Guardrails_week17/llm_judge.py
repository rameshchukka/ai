"""
llm_judge.py
Week 17 - Step 4: LLM-as-judge eval

The rule-based eval_runner.py checks structure (schema, urgency label) but
can't judge whether the suggested_first_response is actually GOOD - grounded,
appropriately toned, free of fabricated promises. That's a judgment call, so
we use a second LLM call with an explicit rubric to score it.

Run: python llm_judge.py
Scores 10 cases and prints results - manually review whether you agree with
the judge, per the Week 17 tutorial's guidance that LLM-as-judge needs
periodic human calibration, not blind trust.
"""

import json
from llm_client import call_llm
from triage_system import classify_ticket
from eval_runner import load_eval_set

JUDGE_SYSTEM = """You are grading a customer support response against a rubric.
Score each criteria from 1 (poor) to 5 (excellent). Return ONLY valid JSON (no
code fences) matching exactly:
{"grounded_in_policy": int, "appropriate_tone": int, "no_fabricated_promises": int,
 "overall": float, "notes": string}

Rubric criteria:
- grounded_in_policy: does the response avoid stating specific policy facts it
  can't actually be certain of (e.g. exact refund amounts, guaranteed timelines)?
- appropriate_tone: is the tone appropriately empathetic/professional for the
  situation (more empathy for angry/urgent tickets, brief and friendly for simple ones)?
- no_fabricated_promises: does the response avoid promising a specific outcome
  (refund approval, exact resolution time) that support can't actually guarantee?
- overall: your holistic 1-5 score
- notes: one sentence explaining your scoring
"""


def judge_response(ticket: str, suggested_response: str) -> dict:
    user_prompt = f"Ticket: {ticket}\n\nSupport agent's suggested first response: {suggested_response}"
    raw = call_llm(JUDGE_SYSTEM, user_prompt, temperature=0.0)
    try:
        cleaned = raw.strip().strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].lstrip("\n")
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"error": "invalid_json", "raw": raw}


if __name__ == "__main__":
    eval_set = load_eval_set()
    sample = eval_set[:10]  # score the first 10 cases

    lines = ["# Results: LLM-as-Judge Scoring\n"]

    for case in sample:
        parsed = classify_ticket(case["ticket"])
        suggested = parsed.get("suggested_first_response", "")
        score = judge_response(case["ticket"], suggested)

        print(f"\n--- {case['id']} ---")
        print(f"Ticket: {case['ticket'][:70]}...")
        print(f"Response: {suggested}")
        print(f"Score: {score}")

        lines.append(f"## {case['id']}\n")
        lines.append(f"**Ticket:** {case['ticket']}\n")
        lines.append(f"**Response:** {suggested}\n")
        lines.append(f"**Judge score:** ```json\n{json.dumps(score, indent=2)}\n```\n")

    lines.append(
        "## Reflection\n\n"
        "_TODO: Pick 3 of the above and manually decide whether you agree with the "
        "judge's score. Where do you disagree, and why? This is the human-calibration "
        "step the Week 17 tutorial describes - LLM-as-judge needs periodic spot-checking "
        "against human judgment, not blind trust._\n"
    )

    with open("results_judge.md", "w") as f:
        f.write("\n".join(lines))
    print("\nResults written to results_judge.md")
