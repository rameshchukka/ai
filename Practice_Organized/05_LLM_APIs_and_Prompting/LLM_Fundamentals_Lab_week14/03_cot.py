"""
03_cot.py
Week 14 - Step 5: Chain-of-thought vs. direct answers

Runs multi-step logic problems two ways: (a) asking directly for the answer,
(b) asking the model to reason step by step first. Compare correctness.

Run: python 03_cot.py
Writes results to results_cot.md

TODO before running: add 2 NEW multi-step logic/billing problems of your own
to BILLING_PROBLEMS (the 2 below are provided as a working example).
"""

from llm_client import call_llm

BILLING_PROBLEMS = [
    "A customer's plan costs $120/month, billed on the 1st. They upgrade to a "
    "$300/month plan on the 15th of a 30-day month. How much is the prorated "
    "charge for the upgrade for the remainder of the month?",
    "A contract renews annually unless cancelled 30 days before the renewal "
    "date. Today is March 1. The renewal date is March 20. Can the customer "
    "still cancel in time to avoid renewal?",
    # TODO: add 2 new problems of your own here
]

DIRECT_SYSTEM = "Answer the question directly and concisely. Do not show your work."

COT_SYSTEM = (
    "Think through this step by step. Show your reasoning, then give your "
    "final answer on a new line prefixed with 'Answer:'."
)


def run_cot_comparison():
    lines = ["# Results: Chain-of-Thought vs. Direct Answers\n"]

    for idx, problem in enumerate(BILLING_PROBLEMS, start=1):
        lines.append(f"## Problem {idx}\n")
        lines.append(f"> {problem}\n")

        direct = call_llm(DIRECT_SYSTEM, problem, temperature=0.0)
        cot = call_llm(COT_SYSTEM, problem, temperature=0.0)

        print(f"=== Problem {idx} ===")
        print("Direct:", direct)
        print("\nCoT:", cot)
        print("\n---\n")

        lines.append(f"**Direct answer:**\n\n{direct}\n")
        lines.append(f"**Chain-of-thought answer:**\n\n{cot}\n")

    lines.append(
        "## Reflection\n\n"
        "_TODO: Did CoT change the final answer for either problem? Note any "
        "cases where the direct answer was wrong and CoT fixed it (or vice versa)._\n"
    )

    with open("results_cot.md", "w") as f:
        f.write("\n".join(lines))
    print("Results written to results_cot.md")


if __name__ == "__main__":
    run_cot_comparison()
