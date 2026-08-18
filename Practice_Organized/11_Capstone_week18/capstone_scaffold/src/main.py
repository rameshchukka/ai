"""
main.py
Capstone scaffold - Week 18, Step 5.

This is deliberately trivial: it just confirms the repo structure, imports,
and (optionally) your LLM provider are all wired correctly BEFORE Month 6's
build sprints start. Replace this with your actual capstone's entry point -
the point of this file is that something runs end-to-end on day one, not
that it does anything interesting yet.

Run: python src/main.py
"""

import sys
import os

# Makes the scaffold runnable from the repo root without extra path setup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def health_check() -> dict:
    """The simplest possible proof-of-life check for this scaffold."""
    checks = {
        "python_version_ok": sys.version_info >= (3, 9),
        "data_dir_exists": os.path.isdir(os.path.join(os.path.dirname(__file__), "..", "data")),
    }

    # Optional: confirm LLM wiring works too, if a provider is configured
    try:
        from llm_client import call_llm, PROVIDER
        reply = call_llm("You are a helpful assistant.", "Reply with just the word 'ready'.")
        checks["llm_provider"] = PROVIDER
        checks["llm_reachable"] = "ready" in reply.lower() or len(reply) > 0
    except Exception as e:
        checks["llm_provider"] = None
        checks["llm_reachable"] = False
        checks["llm_error"] = str(e)

    return checks


if __name__ == "__main__":
    print("Capstone scaffold health check:")
    results = health_check()
    for key, value in results.items():
        print(f"  {key}: {value}")

    if all(v for k, v in results.items() if k in ("python_version_ok", "data_dir_exists")):
        print("\nScaffold structure OK. Ready for Month 6 build sprints.")
    else:
        print("\nSomething's not wired up yet - check the failures above.")
