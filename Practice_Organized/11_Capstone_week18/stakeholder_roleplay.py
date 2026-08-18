"""
stakeholder_roleplay.py
Week 18 - Step 4: Discovery Questions, practiced live

Instead of just writing 5 discovery questions on paper, this script has the
model ROLE-PLAY a non-technical stakeholder in your chosen industry, so you
can practice an actual discovery conversation and see how a real answer
might change your technical design. This is closer to the real skill than
writing questions in isolation - a good question is only good if you know
what to DO with the answer.

Run: python stakeholder_roleplay.py
Type your questions when prompted. Type 'done' to end and get a debrief.
"""

import os
from llm_client import call_llm

INDUSTRY_PERSONAS = {
    "fintech": (
        "You are Sam, a VP of Risk Operations at a mid-size fintech company. You are "
        "NOT technical - you think in terms of fraud loss numbers, compliance audits, "
        "and analyst headcount, not APIs or models. You're cautiously interested in "
        "AI helping your fraud triage team but worried about false positives blocking "
        "legitimate customers and about explainability for regulators."
    ),
    "healthcare": (
        "You are Dr. Chen, a clinic operations manager (not a physician) at a mid-size "
        "healthcare practice. You are NOT technical. You care about patient wait times, "
        "staff burnout from paperwork, and HIPAA compliance above all else. You're "
        "skeptical of anything that could introduce clinical risk."
    ),
    "legal": (
        "You are Morgan, a contracts operations lead at a corporate legal department. "
        "You are NOT technical. You care about turnaround time on contract reviews, "
        "consistency in flagging risky clauses, and NEVER wanting an AI tool to give "
        "something that looks like unauthorized legal advice."
    ),
    "support_ops": (
        "You are Jordan, a Head of Customer Support at a SaaS company. You are NOT "
        "technical. You care about ticket resolution time, CSAT scores, and agent "
        "burnout. You're excited about AI but have been burned before by a chatbot "
        "that gave customers wrong information confidently."
    ),
}

ROLEPLAY_SYSTEM_TEMPLATE = """{persona}

You are being interviewed by someone scoping a potential AI project for your team. Answer
their questions IN CHARACTER, the way a real busy, non-technical stakeholder would -
sometimes vague, sometimes bringing up a concern they didn't ask about, sometimes not
knowing exact numbers off the top of your head. Do NOT be an idealized easy interview -
real discovery calls have some friction and ambiguity. Keep answers to 2-4 sentences.
"""


def run_roleplay(industry: str):
    if industry not in INDUSTRY_PERSONAS:
        print(f"Unknown industry '{industry}'. Choose from: {list(INDUSTRY_PERSONAS.keys())}")
        return

    system_prompt = ROLEPLAY_SYSTEM_TEMPLATE.format(persona=INDUSTRY_PERSONAS[industry])
    transcript = []

    print(f"\nRoleplay started - industry: {industry}")
    print("Ask your discovery questions one at a time. Type 'done' when finished.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() == "done":
            break
        if not question:
            continue

        conversation_context = "\n".join(f"Q: {q}\nA: {a}" for q, a in transcript)
        user_prompt = f"{conversation_context}\n\nNew question: {question}" if transcript else question

        answer = call_llm(system_prompt, user_prompt, temperature=0.7)
        print(f"Stakeholder: {answer}\n")
        transcript.append((question, answer))

    if not transcript:
        print("No questions asked - nothing to debrief.")
        return

    debrief_transcript = "\n".join(f"Q: {q}\nA: {a}" for q, a in transcript)
    debrief_system = """You are a senior FDE coaching a junior FDE on their discovery call
technique. Review the Q&A transcript below and give brief, direct feedback: which questions
were strong (specific, would meaningfully change technical design), which were weak (too
technical/jargon-heavy, too broad, or wouldn't change anything about the build), and what
question they should have asked but didn't."""

    print("=" * 60)
    print("DEBRIEF")
    print("=" * 60)
    feedback = call_llm(debrief_system, debrief_transcript, temperature=0.3)
    print(feedback)

    with open("discovery_transcript.md", "w") as f:
        f.write(f"# Discovery Roleplay Transcript — {industry}\n\n")
        for q, a in transcript:
            f.write(f"**You:** {q}\n\n**Stakeholder:** {a}\n\n")
        f.write(f"## Coach Debrief\n\n{feedback}\n")
    print("\nTranscript + debrief written to discovery_transcript.md")


if __name__ == "__main__":
    print("Available industries:", list(INDUSTRY_PERSONAS.keys()))
    chosen = input("Which industry matches your capstone? ").strip().lower()
    run_roleplay(chosen)
