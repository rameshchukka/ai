"""
regression_test.py
Week 17 - Step 5: Regression test

Deliberately swaps in TRIAGE_SYSTEM_DEGRADED (a plausible "someone simplified
the prompt" edit that drops the anti-prompt-injection instruction) and re-runs
the eval suite, to confirm it actually catches the regression - specifically
on the adversarial subset, where the degraded prompt is expected to fail.

Run: python regression_test.py
Writes results to results_regression_test.md

Note on mock mode: mock_responses.py's lookup is keyed by ticket text, not by
which system prompt was used - which means in PURE mock mode this script
can't actually demonstrate a real behavioral difference (the mock doesn't
know to answer differently for the degraded prompt). This is a real
limitation of simple mocks worth understanding: mock mode is great for
testing your CODE's logic (the eval runner, the scoring, the report
generation), but it cannot substitute for testing actual MODEL behavior
change. Run this against a real provider (gemini_auto or openrouter) to see
the genuine regression - see the note printed at the end of this script.
"""

from triage_system import TRIAGE_SYSTEM, TRIAGE_SYSTEM_DEGRADED
from eval_runner import load_eval_set, run_eval, write_report


if __name__ == "__main__":
    eval_set = load_eval_set()

    print("=" * 60)
    print("BASELINE (real TRIAGE_SYSTEM)")
    print("=" * 60)
    baseline = run_eval(eval_set, system_prompt=TRIAGE_SYSTEM, verbose=False)
    write_report(baseline, path="results_regression_baseline.md", title="Regression Test - Baseline")
    print(f"Baseline: {baseline['summary']}")

    print("\n" + "=" * 60)
    print("DEGRADED (TRIAGE_SYSTEM_DEGRADED - missing injection defense)")
    print("=" * 60)
    degraded = run_eval(eval_set, system_prompt=TRIAGE_SYSTEM_DEGRADED, verbose=False)
    write_report(degraded, path="results_regression_degraded.md", title="Regression Test - Degraded")
    print(f"Degraded: {degraded['summary']}")

    baseline_rate = baseline["summary"]["pass_rate"]
    degraded_rate = degraded["summary"]["pass_rate"]
    baseline_adv_rate = baseline["summary"]["adversarial_pass_rate"]
    degraded_adv_rate = degraded["summary"]["adversarial_pass_rate"]

    with open("results_regression_test.md", "w") as f:
        f.write("# Regression Test: Baseline vs. Degraded Prompt\n\n")
        f.write(f"| | Overall pass rate | Adversarial-subset pass rate |\n")
        f.write(f"|---|---|---|\n")
        f.write(f"| Baseline (real prompt) | {baseline_rate*100:.1f}% | {baseline_adv_rate*100:.1f}% |\n")
        f.write(f"| Degraded (missing injection defense) | {degraded_rate*100:.1f}% | {degraded_adv_rate*100:.1f}% |\n\n")
        if degraded_rate < baseline_rate:
            f.write(
                "**The eval suite caught the regression** - the degraded prompt scored "
                "lower, specifically on the adversarial subset, exactly as expected.\n"
            )
        else:
            f.write(
                "**No difference detected in this run.** If you're in mock mode, this is "
                "expected (see the note in regression_test.py's docstring) - re-run "
                "against a real provider to see the genuine behavioral regression.\n"
            )

    print(f"\nBaseline overall: {baseline_rate*100:.1f}% | Degraded overall: {degraded_rate*100:.1f}%")
    print(f"Baseline adversarial: {baseline_adv_rate*100:.1f}% | Degraded adversarial: {degraded_adv_rate*100:.1f}%")

    if degraded_rate == baseline_rate:
        print(
            "\nNOTE: no difference detected. If LLM_PROVIDER=mock, this is expected - "
            "the mock is keyed by ticket text only, not by which system prompt was used, "
            "so it can't simulate a real degraded-model response. Re-run with "
            "LLM_PROVIDER=gemini_auto to see the real regression on the adversarial cases."
        )

    print("\nResults written to results_regression_test.md")
