"""
07_mock_practice.py
Mock Response Exercises - practicing defensive code against known,
predictable (including deliberately broken) LLM outputs, with no API key
or network call required.

Run: python 07_mock_practice.py
(This script forces mock mode internally regardless of your .env setting,
so it always works offline.)

Why this exercise exists: real LLM outputs are unpredictable by nature - that
makes them great for testing model *behavior*, but annoying for testing your
own *code*. When you're debugging a parser or a pipeline's plumbing, you want
a fixed, known input every time. Mock mode gives you that.
"""

import os
import json

# Force mock mode for this script specifically, regardless of .env
os.environ["LLM_PROVIDER"] = "mock"

from llm_client import call_llm
from mock_responses import CLEAN_JSON_RESPONSE, MESSY_JSON_RESPONSE, BROKEN_JSON_RESPONSE

# Reuse the defensive parser you built in Exercise 4
import importlib
_structured = importlib.import_module("04_structured_output")
parse_llm_json = _structured.parse_llm_json


def exercise_a_predictable_classification():
    """Mock responses are deterministic - same input, same output, every time.
    This is useful for writing unit-test-style checks against your own code."""
    print("=== Exercise A: Predictable Mock Classification ===")
    test_cases = [
        ("The app crashes when I click export.", "Bug"),
        ("Could you add bulk delete?", "Feature Request"),
        ("How do I change my email?", "Question"),
    ]
    classify_system = "Classify this feedback as Bug, Feature Request, or Question."

    all_passed = True
    for message, expected in test_cases:
        result = call_llm(classify_system, message)
        passed = expected.lower() in result.lower()
        all_passed = all_passed and passed
        print(f"  input={message!r:45} expected={expected:16} got={result!r:16} {'PASS' if passed else 'FAIL'}")

    print(f"\nAll passed: {all_passed}\n")


def exercise_b_defensive_parsing_against_known_failures():
    """Test your parser directly against known-good, known-messy, and
    known-broken responses - without needing the model to cooperate by
    accident. This is exactly how you'd build a regression test suite."""
    print("=== Exercise B: Defensive Parsing Against Known Failure Modes ===")

    cases = {
        "clean": CLEAN_JSON_RESPONSE,
        "messy (code fences + preamble)": MESSY_JSON_RESPONSE,
        "broken (invalid JSON on purpose)": BROKEN_JSON_RESPONSE,
    }

    for label, raw in cases.items():
        print(f"\n--- {label} ---")
        print("Raw:", raw[:80], "..." if len(raw) > 80 else "")
        parsed = parse_llm_json(raw)
        print("Parsed:", parsed)

        if label == "messy (code fences + preamble)" and "error" in parsed:
            print(
                "NOTE: this one failed on purpose - your Exercise 4 parser only "
                "strips code fences when the response STARTS with them. A real "
                "preamble sentence before the fence ('Sure, here's...') defeats it. "
                "This is exactly the production-hardening gap Exercise 4's "
                "Reflection question asks about - fix parse_llm_json() in "
                "04_structured_output.py to search for a ```json block anywhere "
                "in the string, then re-run this script to confirm the fix."
            )

        if label == "broken (invalid JSON on purpose)":
            assert "error" in parsed, "Your parser should catch this, not crash or silently return bad data!"
            print("Confirmed: parser correctly caught the broken JSON instead of crashing.")


def exercise_c_compare_mock_vs_real():
    """A prompt for you to run twice: once here (mock), once with the real
    Exercise 1 script against live Gemini. Compare the *shape* of the output,
    not the exact words - mock responses are realistic but not generated."""
    print("=== Exercise C: Mock vs. Real (do this comparison yourself) ===")
    result = call_llm(
        system="You are a creative writing assistant.",
        user="Write a one-sentence tagline for a coffee shop.",
    )
    print("Mock tagline:", result)
    print(
        "\nTODO: Now run `python 01_temperature.py` with LLM_PROVIDER=gemini in your "
        ".env, and compare: does the real Gemini output feel meaningfully different "
        "in tone/creativity from this mock tagline? Write 2 sentences on what mock "
        "mode is good for testing vs. what it can't tell you."
    )


if __name__ == "__main__":
    exercise_a_predictable_classification()
    exercise_b_defensive_parsing_against_known_failures()
    exercise_c_compare_mock_vs_real()
