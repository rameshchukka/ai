"""
grounding_stress_test.py
Week 15 - Part B, Step 4: Refusal / grounding stress test

Asks 5 plausible-sounding questions that are NOT answerable from the policy
documents, and checks whether the RAG system correctly refuses to guess
rather than hallucinating a confident-sounding wrong answer.

Run: python grounding_stress_test.py
Writes results to results_grounding.md
"""

from generate import answer_question

# TODO: these 5 are provided as a working example - all are plausible support
# questions with NO answer in the docs/ policy set. Feel free to add your own.
UNANSWERABLE_QUESTIONS = [
    "Do you offer a price-match guarantee if I find the item cheaper elsewhere?",
    "Can I pay for my subscription in cryptocurrency?",
    "What's your policy on customers who are minors making purchases?",
    "Do you offer a military or student discount?",
    "Can I transfer my extended warranty to someone else if I sell the product?",
]

REFUSAL_MARKERS = [
    "don't have information",
    "not covered",
    "no information",
    "not specified",
    "cannot find",
    "does not mention",
]


def looks_like_a_refusal(answer: str) -> bool:
    lowered = answer.lower()
    return any(marker in lowered for marker in REFUSAL_MARKERS)


def run_stress_test():
    lines = ["# Results: Grounding Stress Test\n"]
    pass_count = 0

    for question in UNANSWERABLE_QUESTIONS:
        result = answer_question(question)
        refused = looks_like_a_refusal(result["answer"])
        status = "PASS (refused correctly)" if refused else "CHECK MANUALLY (may have guessed)"
        if refused:
            pass_count += 1

        print(f"\nQ: {question}")
        print(f"A: {result['answer']}")
        print(f"Status: {status}")

        lines.append(f"## {question}\n")
        lines.append(f"**Answer:** {result['answer']}\n")
        lines.append(f"**Status:** {status}\n")

    lines.append(f"\n## Summary\n\n{pass_count}/{len(UNANSWERABLE_QUESTIONS)} auto-detected as correct refusals.\n")
    lines.append(
        "_Note: the refusal-phrase detector above is a simple heuristic, not a "
        "reliable eval - manually read every answer above, since the model could "
        "phrase a refusal differently, or worse, could hallucinate a plausible-"
        "sounding wrong answer that doesn't trip any of the refusal markers._\n"
    )
    lines.append(
        "## Reflection\n\n"
        "_TODO: Did the system correctly refuse on all 5? If it hallucinated on "
        "any, what would you change in the system prompt (RAG_SYSTEM_TEMPLATE in "
        "generate.py) to fix it? Try tightening the wording and re-running._\n"
    )

    with open("results_grounding.md", "w") as f:
        f.write("\n".join(lines))
    print(f"\n{pass_count}/{len(UNANSWERABLE_QUESTIONS)} auto-detected as correct refusals.")
    print("Full results written to results_grounding.md")


if __name__ == "__main__":
    run_stress_test()
