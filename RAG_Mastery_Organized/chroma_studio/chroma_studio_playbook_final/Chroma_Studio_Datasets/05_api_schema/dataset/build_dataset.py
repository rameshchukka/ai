"""
build_dataset.py — API Schema Dataset (Phase 2: request/response detail)
========================================================================
Phase 1 answered "WHICH endpoint does X?" (one row per endpoint, embed the purpose).
Phase 2 answers "HOW do I call it?" — parameters, request body, responses, errors.

THE KEY DESIGN DIFFERENCE FROM PHASE 1
--------------------------------------
Phase 1: one endpoint = one document (its purpose).
Phase 2: one endpoint = SEVERAL documents, one per schema aspect:
    - params    : path/query parameters
    - request   : request body fields
    - response  : success response fields
    - errors    : error codes and meanings
Why chunk this way? Because schema questions are aspect-scoped: "what fields does
the refund body take?" wants the REQUEST chunk, "what errors can it return?" wants
the ERRORS chunk. One giant per-endpoint blob would force every query to wade
through irrelevant schema. Splitting by aspect makes retrieval precise AND lets you
filter by aspect in Chroma Studio.

Metadata (richer than Phase 1, to support aspect-scoped retrieval):
    - endpoint  : the path (join key back to Phase 1)
    - method    : HTTP method
    - domain    : service area
    - aspect    : params | request | response | errors   <-- NEW, the chunk type
    - version   : v1 / v2
    - status    : active / deprecated

Output: dataset/api_schema_chunks.csv
Columns: id, text, endpoint, method, domain, aspect, version, status
"""
import csv, os

rows = []
def add(id, text, endpoint, method, domain, aspect, version="v1", status="active"):
    rows.append(dict(id=id, text=text, endpoint=endpoint, method=method,
                     domain=domain, aspect=aspect, version=version, status=status))

# ==========================================================================
# Each endpoint below expands into up to 4 aspect-chunks. We cover a
# representative subset of Phase 1's catalog in schema depth (not all 30 —
# in real life you'd generate these from the OpenAPI spec).
# ==========================================================================

# ---- POST /v1/payments  (create payment) ---------------------------------
EP = "/v1/payments"; DOM = "payments"; M = "POST"
add("pay_create_params", "Create payment has no path or query parameters; all input is in the request body.", EP, M, DOM, "params")
add("pay_create_request",
    "Create payment request body fields: amount (integer, minor units, required); currency (string, ISO-4217, required); "
    "customer_id (string, required); source (string, card or account token, required); description (string, optional); "
    "metadata (object, optional key-value pairs).", EP, M, DOM, "request")
add("pay_create_response",
    "Create payment success response (201): id (string, payment id); status (string, one of authorized, captured, failed); "
    "amount (integer); currency (string); created_at (timestamp). Returns the created payment resource.", EP, M, DOM, "response")
add("pay_create_errors",
    "Create payment errors: 400 invalid_amount if amount <= 0; 402 card_declined if the source is refused; "
    "409 duplicate_request if the idempotency key was already used; 422 missing_field for absent required fields.", EP, M, DOM, "errors")

# ---- POST /v1/payments/{id}/refund  (refund) -----------------------------
EP = "/v1/payments/{id}/refund"; DOM = "payments"; M = "POST"
add("pay_refund_params", "Refund payment path parameter: id (string, required) — the payment id to refund. No query parameters.", EP, M, DOM, "params")
add("pay_refund_request",
    "Refund payment request body fields: amount (integer, optional; omit for a full refund, provide for partial); "
    "reason (string, optional, e.g. requested_by_customer, duplicate, fraudulent).", EP, M, DOM, "request")
add("pay_refund_response",
    "Refund payment success response (201): id (string, refund id); payment_id (string); amount (integer refunded); "
    "status (string, one of pending, succeeded, failed); created_at (timestamp).", EP, M, DOM, "response")
add("pay_refund_errors",
    "Refund payment errors: 404 payment_not_found; 400 amount_exceeds_refundable if amount is larger than the remaining "
    "captured balance; 409 already_refunded if the payment was fully refunded.", EP, M, DOM, "errors")

# ---- GET /v1/payments/{id}  (get payment) --------------------------------
EP = "/v1/payments/{id}"; DOM = "payments"; M = "GET"
add("pay_get_params", "Get payment path parameter: id (string, required). Optional query parameter expand (string) to inline related objects.", EP, M, DOM, "params")
add("pay_get_response",
    "Get payment response (200): id, status, amount, currency, customer_id, source, created_at, and a refunds array if any.", EP, M, DOM, "response")
add("pay_get_errors", "Get payment errors: 404 payment_not_found if the id does not exist; 401 unauthorized if the token is missing or invalid.", EP, M, DOM, "errors")

# ---- POST /v1/cards  (issue card) ----------------------------------------
EP = "/v1/cards"; DOM = "cards"; M = "POST"
add("card_issue_params", "Issue card has no path or query parameters; input is in the request body.", EP, M, DOM, "params")
add("card_issue_request",
    "Issue card request body: account_id (string, required); type (string, required, one of virtual, physical); "
    "cardholder_name (string, required); currency (string, ISO-4217, required); spending_limit (integer, optional, minor units).", EP, M, DOM, "request")
add("card_issue_response",
    "Issue card response (201): id (string, card id); last4 (string); type (string); status (string, one of active, inactive); "
    "account_id (string); created_at (timestamp). Full PAN is never returned.", EP, M, DOM, "response")
add("card_issue_errors",
    "Issue card errors: 404 account_not_found; 422 missing_field; 403 kyc_incomplete if the account holder has not passed KYC.", EP, M, DOM, "errors")

# ---- POST /v1/cards/{id}/freeze  (freeze card) ---------------------------
EP = "/v1/cards/{id}/freeze"; DOM = "cards"; M = "POST"
add("card_freeze_params", "Freeze card path parameter: id (string, required) — the card id to freeze. No request body.", EP, M, DOM, "params")
add("card_freeze_response", "Freeze card response (200): id (string); status (string, will be frozen); frozen_at (timestamp).", EP, M, DOM, "response")
add("card_freeze_errors", "Freeze card errors: 404 card_not_found; 409 already_frozen if the card is already frozen.", EP, M, DOM, "errors")

# ---- POST /v1/oauth/token  (get token) -----------------------------------
EP = "/v1/oauth/token"; DOM = "auth"; M = "POST"
add("auth_token_request",
    "OAuth token request body (form-encoded): grant_type (string, required, e.g. client_credentials); client_id (string, required); "
    "client_secret (string, required); scope (string, optional, space-separated scopes).", EP, M, DOM, "request", status="active")
add("auth_token_response",
    "OAuth token response (200): access_token (string); token_type (string, Bearer); expires_in (integer seconds, e.g. 3600); "
    "scope (string, granted scopes).", EP, M, DOM, "response")
add("auth_token_errors",
    "OAuth token errors: 400 invalid_request for malformed body; 401 invalid_client for bad client_id/secret; "
    "400 unsupported_grant_type for an unknown grant_type.", EP, M, DOM, "errors")

# ---- POST /v2/payments  (create payment v2) ------------------------------
EP = "/v2/payments"; DOM = "payments"; M = "POST"
add("pay_create_v2_request",
    "Create payment v2 request body: same as v1 (amount, currency, customer_id, source, description, metadata) plus a required "
    "Idempotency-Key header to safely retry without double-charging.", EP, M, DOM, "request", version="v2")
add("pay_create_v2_response",
    "Create payment v2 response (201): same fields as v1 create payment, plus idempotency_key echoed back.", EP, M, DOM, "response", version="v2")

out = os.path.join(os.path.dirname(__file__) or ".", "dataset", "api_schema_chunks.csv")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id","text","endpoint","method","domain","aspect","version","status"])
    w.writeheader(); w.writerows(rows)

print(f"Wrote {len(rows)} schema chunks to {out}")
from collections import Counter
for field in ["aspect","domain","method","version","status"]:
    print(f"  {field}:", dict(Counter(r[field] for r in rows)))
print(f"  distinct endpoints: {len(set(r['endpoint'] for r in rows))}")
