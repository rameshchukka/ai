"""
05_context_management.py
Week 14 - Step 7: Context management

Summarizes 3 independent "documents," then stress-tests context management by
combining all 3 summaries into one prompt and asking a question that requires
synthesizing across all of them correctly.

Run: python 05_context_management.py
Writes results to results_context.md
"""

from llm_client import call_llm

DOCUMENTS = {
    "doc_a": """Refund Policy: Customers may request a full refund within 14 days
    of purchase. After 14 days, only store credit is issued, and only for unopened
    items. Digital goods are non-refundable after download.""",
    "doc_b": """Shipping Policy: Standard shipping takes 5-7 business days.
    Express shipping (additional $12) takes 1-2 business days. International
    orders may take up to 21 business days and are not eligible for express shipping.""",
    "doc_c": """Warranty Policy: All hardware products include a 1-year limited
    warranty covering manufacturing defects. Accidental damage is not covered.
    Extended warranties (up to 3 years) can be purchased within 30 days of the
    original purchase.""",
}

SUMMARIZE_SYSTEM = (
    "Summarize the following policy in under 40 words, preserving the most "
    "decision-relevant facts (numbers, deadlines, exceptions)."
)

QUESTION = (
    "A customer in Germany bought a hardware item 10 days ago, wants express "
    "international shipping on a replacement, and is asking whether they can "
    "also get a 3-year extended warranty. Answer each part."
)


def run_context_management():
    lines = ["# Results: Context Management\n", "## Summaries\n"]

    summaries = {}
    for name, text in DOCUMENTS.items():
        summary = call_llm(SUMMARIZE_SYSTEM, text, temperature=0.0)
        summaries[name] = summary
        print(f"--- {name} ---\n{summary}\n")
        lines.append(f"**{name}:** {summary}\n")

    combined_context = "\n\n".join(f"{k}: {v}" for k, v in summaries.items())

    synthesis_system = f"""Answer using ONLY the policies below. If the answer isn't
covered, say so explicitly rather than guessing.

{combined_context}
"""

    print("=== Synthesis question ===")
    print(QUESTION)
    answer = call_llm(synthesis_system, QUESTION, temperature=0.0)
    print("\nAnswer:\n", answer)

    lines.append(f"## Synthesis Question\n\n> {QUESTION}\n")
    lines.append(f"**Answer:**\n\n{answer}\n")

    lines.append(
        "## Reflection\n\n"
        "_TODO: Did the model correctly use facts from all three summarized "
        "policies, or did it drop/blend anything? This is the 'lost in the "
        "middle' effect - note anything that went wrong and how you'd fix it "
        "(clearer delimiters, explicit per-policy instructions, etc.)._\n"
    )

    with open("results_context.md", "w") as f:
        f.write("\n".join(lines))
    print("\nResults written to results_context.md")


if __name__ == "__main__":
    run_context_management()
