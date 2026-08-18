"""
02_classifier.py
Week 14 - Step 4: Zero-shot vs. few-shot classification

Classifies customer feedback as Bug / Feature Request / Question, first with
a zero-shot prompt, then with a few-shot prompt, so you can compare accuracy
and consistency directly.

Run: python 02_classifier.py
Writes results to results_classifier.md

TODO before running: add 5 NEW test tickets of your own to TEST_MESSAGES
(the 5 below are provided as a working example - replace or extend them).
"""

from llm_client import call_llm

TEST_MESSAGES = [
    "The export button crashes the app every time I click it.",
    "It would be great if I could bulk-delete old projects.",
    "How do I change my billing email address?",
    "None of my recent uploads are showing up, is this a known issue?",
    "Can you add dark mode to the mobile app?",
    # TODO: add your own new test tickets here
]

ZERO_SHOT_SYSTEM = (
    "Classify the customer feedback as Bug, Feature Request, or Question. "
    "Reply with only the label."
)

FEW_SHOT_SYSTEM = """Classify customer feedback as Bug, Feature Request, or Question.
Reply with only the label.

Feedback: "The app freezes when I upload a file over 10MB."
Label: Bug

Feedback: "Could you let us export reports as CSV?"
Label: Feature Request

Feedback: "Where do I find my invoice history?"
Label: Question
"""


def run_classifier():
    lines = ["# Results: Zero-shot vs. Few-shot Classifier\n"]

    lines.append("## Zero-shot\n")
    print("=== Zero-shot ===")
    zero_shot_results = []
    for msg in TEST_MESSAGES:
        result = call_llm(ZERO_SHOT_SYSTEM, msg, temperature=0.0).strip()
        zero_shot_results.append(result)
        print(f"- {msg[:55]!r:60} -> {result}")
        lines.append(f"- `{msg}` -> **{result}**")

    lines.append("\n## Few-shot\n")
    print("\n=== Few-shot ===")
    few_shot_results = []
    for msg in TEST_MESSAGES:
        result = call_llm(FEW_SHOT_SYSTEM, msg, temperature=0.0).strip()
        few_shot_results.append(result)
        print(f"- {msg[:55]!r:60} -> {result}")
        lines.append(f"- `{msg}` -> **{result}**")

    lines.append("\n## Differences\n")
    diffs = [
        (msg, z, f)
        for msg, z, f in zip(TEST_MESSAGES, zero_shot_results, few_shot_results)
        if z != f
    ]
    if diffs:
        for msg, z, f in diffs:
            lines.append(f"- `{msg}`: zero-shot=**{z}**, few-shot=**{f}**")
    else:
        lines.append("_No differences between zero-shot and few-shot on this test set._")

    lines.append(
        "\n## Reflection\n\n"
        "_TODO: Which classifications changed between zero-shot and few-shot? "
        "Why do you think the examples helped (or didn't)?_\n"
    )

    with open("results_classifier.md", "w") as f:
        f.write("\n".join(lines))
    print("\nResults written to results_classifier.md")


if __name__ == "__main__":
    run_classifier()
