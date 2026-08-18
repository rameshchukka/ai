"""
01_temperature.py
Week 14 - Step 3: Temperature experiment

Runs the same creative prompt 3x at temperature 0.0 and 3x at temperature 1.0,
so you can directly compare determinism vs. variability.

Run: python 01_temperature.py
Writes results to results_temperature.md
"""

from llm_client import call_llm

PROMPT_SYSTEM = "You are a creative writing assistant."
PROMPT_USER = "Write a one-sentence tagline for a coffee shop."


def run_experiment():
    lines = ["# Results: Temperature Experiment\n"]

    lines.append("## Temperature 0.0 (x3)\n")
    print("=== Temperature 0.0 (x3) ===")
    for i in range(3):
        result = call_llm(PROMPT_SYSTEM, PROMPT_USER, temperature=0.0)
        print(f"{i + 1}: {result}")
        lines.append(f"{i + 1}. {result}")

    lines.append("\n## Temperature 1.0 (x3)\n")
    print("\n=== Temperature 1.0 (x3) ===")
    for i in range(3):
        result = call_llm(PROMPT_SYSTEM, PROMPT_USER, temperature=1.0)
        print(f"{i + 1}: {result}")
        lines.append(f"{i + 1}. {result}")

    lines.append(
        "\n## Reflection\n\n"
        "_TODO: Did the temperature-0 runs come back identical or near-identical? "
        "Did the temperature-1.0 runs vary more in wording, structure, or tone? "
        "Name one real FDE scenario where you'd deliberately pick temperature 0 "
        "vs. a higher temperature._\n"
    )

    with open("results_temperature.md", "w") as f:
        f.write("\n".join(lines))
    print("\nResults written to results_temperature.md")


if __name__ == "__main__":
    run_experiment()
