# Validation Scorecard — Human-Completed Checks
## API Governance & Discovery Platform

**This file covers the validation layers that cannot be automated.**
Fill in each section as you complete it. Keep this as the official
pre-launch sign-off record.

---

## Layer 1 — Ingestion Quality Spot-Check

Reviewer: ___________________________  Date: _______________

Pick 15 APIs at random from your real ingested data. For each, open the
raw Bitbucket spec and compare against what was ingested.

| API project_name | purpose_text accurate? | functionality correct? | domain correct? | req fields match spec? | resp fields match spec? | Pass? |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |

**Pass count:** _____ / 15   (minimum 13 to pass)

**Common failure notes:**
_____________________________________________________________

**Action taken if failed:**
_____________________________________________________________

**Layer 1 result:** [ ] PASS  [ ] FAIL

---

## Layer 3 — Composition Correctness (Architect Review)

Reviewer: ___________________________  Date: _______________

Review the first 20 COMPOSE recommendations in the Merge Candidates screen.
For each, mark whether the proposed composition is genuinely valid.

| composition_id | APIs proposed | Approved? | If rejected: reason |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

**Approved count:** _____ / 20   (minimum 14 to pass)

**Rejection patterns (common reasons):**
_____________________________________________________________

**Threshold adjustment needed?**
[ ] No — scores are well calibrated
[ ] Yes — raise domain_alignment weight (too many cross-domain false positives)
[ ] Yes — raise schema_compat threshold (field matches too loose)
[ ] Yes — reduce similarity threshold (results too narrow)

**Layer 3 result:** [ ] PASS  [ ] FAIL

---

## Layer 6 — Phase 1 Rule Correctness (Architect Review)

Reviewer: ___________________________  Date: _______________

Review the first 30 structural findings in the Findings Dashboard.
For each, mark whether it is a genuine governance issue or a false positive.

| finding_id | pattern_type | Genuine? | If false positive: reason |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

**Genuine finding count:** _____ / 30   (minimum 21 to pass = 70%)

**Most common false positive type:**
[ ] API version pairs (M1b version detection issue)
[ ] Healthy fan-in reuse (raise FAN_IN_THRESHOLD)
[ ] Pass-through with real transformation logic (add has_transformation flag)
[ ] Deep chain that is legitimately architectured (raise DEEP_CHAIN_THRESHOLD)

**Threshold changes recommended:**
_____________________________________________________________

**Layer 6 result:** [ ] PASS  [ ] FAIL

---

## Go-Live Sign-Off

All checks below must be marked PASS before the platform is opened to developers.

| Layer | Check | Result | Sign-off |
|---|---|---|---|
| 1 — Ingestion accuracy | 13/15 spot-check pass | [ ] PASS  [ ] FAIL | |
| 2 — Retrieval recall@3 | 18/25 labelled test pass (Notebook 2) | [ ] PASS  [ ] FAIL | |
| 3 — Composition approval | 14/20 COMPOSE approved | [ ] PASS  [ ] FAIL | |
| 4 — Embedding gap | gap > 0.10 (Notebook 1) | [ ] PASS  [ ] FAIL | |
| 5 — Graph correctness | 5/5 flows exact (Notebook 1) | [ ] PASS  [ ] FAIL | |
| 6 — Phase 1 genuine rate | 21/30 findings genuine | [ ] PASS  [ ] FAIL | |
| 7 — Audit trail integrity | All 5 workflow tests pass (Notebook 3) | [ ] PASS  [ ] FAIL | |
| 8 — LLM band stability | Max 1 variation in 5 runs (Notebook 1) | [ ] PASS  [ ] FAIL | |

**Overall go-live decision:**

[ ] **APPROVED** — all 8 layers pass. Platform is ready for developer access.

[ ] **CONDITIONAL** — warnings only, no failures. Proceed with monitoring plan.

[ ] **NOT APPROVED** — one or more layers failed. Fix and re-validate before launch.

**Approved by:** _________________________  **Date:** _______________

**Notes:**
_____________________________________________________________
