"""
eval_runner.py
Week 17 - Step 2: Rule-based eval runner

Loads eval_set.json, runs every ticket through the triage system, and checks:
  1. Schema validity (valid JSON, all required keys present, urgency is a
     real enum value)
  2. Exact-match urgency (does it match expected_urgency, where specified -
     adversarial cases with expected_urgency=null only get the schema check,
     since the "correct" urgency for a pure injection-resistance test is
     more about NOT breaking than about matching one specific label)

Run: python eval_runner.py
Writes results to results_baseline.md
"""

import json
from triage_system import classify_ticket, is_schema_valid, TRIAGE_SYSTEM


def load_eval_set(path: str = "eval_set.json") -> list:
    with open(path) as f:
        return json.load(f)


def run_eval(eval_set: list, system_prompt: str = TRIAGE_SYSTEM, verbose: bool = True) -> dict:
    results = []

    for case in eval_set:
        parsed = classify_ticket(case["ticket"], system_prompt=system_prompt)
        schema_ok = is_schema_valid(parsed)

        urgency_ok = None
        if case["expected_urgency"] is not None:
            urgency_ok = schema_ok and parsed.get("urgency") == case["expected_urgency"]

        passed = schema_ok and (urgency_ok in (True, None))

        results.append({
            "id": case["id"],
            "adversarial": case["adversarial"],
            "schema_valid": schema_ok,
            "urgency_match": urgency_ok,
            "passed": passed,
            "expected_urgency": case["expected_urgency"],
            "actual_urgency": parsed.get("urgency"),
            "notes": case["notes"],
        })

        if verbose:
            status = "PASS" if passed else "FAIL"
            print(f"[{status}] {case['id']:5} adversarial={case['adversarial']!s:5} "
                  f"expected={str(case['expected_urgency']):8} actual={str(parsed.get('urgency')):8}")

    total = len(results)
    passed_count = sum(1 for r in results if r["passed"])
    adversarial_results = [r for r in results if r["adversarial"]]
    adversarial_passed = sum(1 for r in adversarial_results if r["passed"])

    summary = {
        "total": total,
        "passed": passed_count,
        "pass_rate": passed_count / total if total else 0,
        "adversarial_total": len(adversarial_results),
        "adversarial_passed": adversarial_passed,
        "adversarial_pass_rate": adversarial_passed / len(adversarial_results) if adversarial_results else 0,
    }

    return {"results": results, "summary": summary}


def write_report(eval_output: dict, path: str = "results_baseline.md", title: str = "Baseline Eval Results"):
    summary = eval_output["summary"]
    lines = [f"# {title}\n"]
    lines.append(
        f"**Overall: {summary['passed']}/{summary['total']} passed "
        f"({summary['pass_rate']*100:.1f}%)**\n"
    )
    lines.append(
        f"**Adversarial subset: {summary['adversarial_passed']}/{summary['adversarial_total']} passed "
        f"({summary['adversarial_pass_rate']*100:.1f}%)**\n"
    )
    lines.append("| ID | Adversarial | Schema Valid | Expected | Actual | Passed |")
    lines.append("|---|---|---|---|---|---|")
    for r in eval_output["results"]:
        lines.append(
            f"| {r['id']} | {r['adversarial']} | {r['schema_valid']} | "
            f"{r['expected_urgency']} | {r['actual_urgency']} | {r['passed']} |"
        )

    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"\nReport written to {path}")


if __name__ == "__main__":
    eval_set = load_eval_set()
    output = run_eval(eval_set)
    write_report(output)
    print(f"\nSummary: {output['summary']}")
