"""
generate.py
Week 15 - Part B, Steps 1-3: Augmented generation + citations

The full RAG answer pipeline: retrieve top-k chunks for a question, build a
prompt with clearly delimited context, ask the model to answer ONLY from that
context and cite which source(s) it used.

Run: python generate.py
Requires: you've already run `python ingest.py` at least once.
"""

from llm_client import call_llm
from retrieve import retrieve, KNOWN_ANSWER_QUERIES

RAG_SYSTEM_TEMPLATE = """You are a support policy assistant. Answer the question using
ONLY the policy excerpts provided below. If the answer isn't covered in these excerpts,
say "I don't have information on that in the available policies" rather than guessing.

For every claim you make, cite the source filename in brackets, e.g. [refund_policy.txt].

--- POLICY EXCERPTS ---
{context}
--- END POLICY EXCERPTS ---
"""


def build_context_block(hits: list) -> str:
    blocks = []
    for h in hits:
        blocks.append(f"[Source: {h['source']}]\n{h['text']}")
    return "\n\n".join(blocks)


def answer_question(question: str, top_k: int = 3) -> dict:
    hits = retrieve(question, top_k=top_k)
    context = build_context_block(hits)
    system_prompt = RAG_SYSTEM_TEMPLATE.format(context=context)

    answer = call_llm(system_prompt, question, temperature=0.0)

    return {
        "question": question,
        "answer": answer,
        "sources_retrieved": [h["source"] for h in hits],
    }


if __name__ == "__main__":
    for query in KNOWN_ANSWER_QUERIES:
        result = answer_question(query)
        print(f"\n=== Q: {result['question']} ===")
        print(f"Retrieved from: {result['sources_retrieved']}")
        print(f"A: {result['answer']}")
