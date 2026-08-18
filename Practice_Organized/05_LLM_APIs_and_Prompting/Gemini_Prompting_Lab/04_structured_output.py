"""
04_structured_output.py
Week 14 - Step 6: Structured output + defensive parsing

Extracts structured JSON from a fictional contract paragraph, then parses it
defensively (handles markdown code fences, invalid JSON, missing fields)
so a malformed response never crashes the pipeline.

Run: python 04_structured_output.py
Writes results to results_structured_output.md
"""

import json
from llm_client import call_llm

# TODO: feel free to replace this with your own fictional contract text.
FICTIONAL_CONTRACT = """
Acme Robotics Inc. agrees to a 24-month service contract with Beta Manufacturing,
valued at $480,000 total, renewing automatically on January 15, 2027 unless
cancelled with 60 days' notice. Beta Manufacturing must maintain minimum order
volumes of $15,000/month or Acme may terminate with 30 days' notice.
"""

EXTRACTION_SYSTEM = """You extract structured data from contract text.
Return ONLY valid JSON, no markdown code fences, no explanation, matching exactly
this shape:
{"company_name": string, "contract_value": string, "renewal_date": string, "risk_flags": [string]}

If a field cannot be determined, use an empty string or empty list - never invent data.
"""


def parse_llm_json(raw_text: str) -> dict:
    """
    Defensive JSON parser for LLM output.
    Strips markdown code fences if present, attempts json.loads(), and on
    failure returns a clear error dict instead of raising - so a malformed
    response never crashes a production pipeline.
    """
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[len("json"):].lstrip("\n")

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print("PARSE FAILURE - raw text was:\n", raw_text)
        return {"error": "invalid_json", "detail": str(e), "raw": raw_text}


def run_extraction():
    lines = ["# Results: Structured Output + Defensive Parsing\n"]

    raw_response = call_llm(EXTRACTION_SYSTEM, FICTIONAL_CONTRACT, temperature=0.0)
    print("Raw model output:\n", raw_response)
    lines.append(f"**Raw model output:**\n\n```\n{raw_response}\n```\n")

    parsed = parse_llm_json(raw_response)
    print("\nParsed:", parsed)
    lines.append(f"**Parsed result:**\n\n```json\n{json.dumps(parsed, indent=2)}\n```\n")

    # Deliberate break test: ask for a response likely to be messier
    print("\n--- Deliberate break test ---")
    messy_system = EXTRACTION_SYSTEM + "\nAlso include a brief one-sentence explanation before the JSON."
    messy_response = call_llm(messy_system, FICTIONAL_CONTRACT, temperature=0.7)
    print("Raw (messy) output:\n", messy_response)
    messy_parsed = parse_llm_json(messy_response)
    print("\nParsed (messy):", messy_parsed)

    lines.append("## Deliberate Break Test\n")
    lines.append(f"**Raw (messy) output:**\n\n```\n{messy_response}\n```\n")
    lines.append(f"**Parsed (messy):**\n\n```json\n{json.dumps(messy_parsed, indent=2)}\n```\n")

    lines.append(
        "## Reflection\n\n"
        "_TODO: Did the model's raw output need any cleanup before json.loads() "
        "worked? What would you add to make this parser more production-grade "
        "(hint: retries, schema validation with pydantic, structured logging)?_\n"
    )

    with open("results_structured_output.md", "w") as f:
        f.write("\n".join(lines))
    print("\nResults written to results_structured_output.md")


if __name__ == "__main__":
    run_extraction()
