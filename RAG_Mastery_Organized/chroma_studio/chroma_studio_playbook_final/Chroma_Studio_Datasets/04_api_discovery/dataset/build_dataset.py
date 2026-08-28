"""
build_dataset.py — API Discovery Dataset (Phase 1: purpose + endpoint)
=======================================================================
A realistic enterprise API catalog for a bank-like org, designed for RAG
discovery: "which API does X?" Each row is ONE endpoint described by its
PURPOSE (what it does, in natural language a developer would search for),
plus discovery-oriented metadata.

Phase 1 scope (this file): purpose + endpoint discovery.
Phase 2 (later, separate): request/response schema & parameter detail.

Design decisions (documented so this reads as a designed artifact, not a dump):
- `text` = a natural-language purpose statement, because discovery queries are
  phrased by intent ("refund a payment"), not by endpoint path. Embedding the
  PURPOSE is what makes semantic discovery work.
- Metadata chosen for filtering in Chroma Studio: `domain`, `method`. Plus
  `endpoint`, `auth`, `version`, `status` carried for realism and Phase 2.
- Deliberate structure planted for examination in Studio:
    * near-duplicate purposes across versions (v1 vs v2 of the same capability)
    * one deprecated endpoint (status filtering demo)
    * cross-domain overlap (notifications touched by two domains)
    * endpoints that read similarly but differ (collision)
  These let Studio's analyze->decide->act loop surface real decisions.

Output: dataset/api_catalog.csv
Columns: id, text, endpoint, method, domain, auth, version, status
"""
import csv, os

rows = []
def add(id, text, endpoint, method, domain, auth, version="v1", status="active"):
    rows.append(dict(id=id, text=text, endpoint=endpoint, method=method,
                     domain=domain, auth=auth, version=version, status=status))

# payments
add("pay_create_01", "Create a new payment to charge a customer's card or account for a given amount and currency.", "/v1/payments", "POST", "payments", "oauth2")
add("pay_get_01", "Retrieve the current status and details of a single payment by its payment id.", "/v1/payments/{id}", "GET", "payments", "oauth2")
add("pay_list_01", "List and search payments filtered by date range, status, or customer.", "/v1/payments", "GET", "payments", "oauth2")
add("pay_refund_01", "Refund a previously captured payment, fully or partially, back to the original method.", "/v1/payments/{id}/refund", "POST", "payments", "oauth2")
add("pay_capture_01", "Capture an authorized-but-uncaptured payment to actually move the funds.", "/v1/payments/{id}/capture", "POST", "payments", "oauth2")
add("pay_create_02", "Create a payment to charge a customer for an amount in a specified currency (v2 with idempotency keys).", "/v2/payments", "POST", "payments", "oauth2", version="v2")

# cards
add("card_issue_01", "Issue a new virtual or physical card to a cardholder under an account.", "/v1/cards", "POST", "cards", "oauth2")
add("card_get_01", "Fetch the details and status of a specific card by card id.", "/v1/cards/{id}", "GET", "cards", "oauth2")
add("card_freeze_01", "Freeze or temporarily block a card to prevent further transactions.", "/v1/cards/{id}/freeze", "POST", "cards", "oauth2")
add("card_unfreeze_01", "Unfreeze a previously blocked card to resume transactions.", "/v1/cards/{id}/unfreeze", "POST", "cards", "oauth2")
add("card_pin_01", "Set or reset the PIN for a card securely.", "/v1/cards/{id}/pin", "PUT", "cards", "oauth2")

# accounts
add("acct_create_01", "Open a new customer account of a given type and currency.", "/v1/accounts", "POST", "accounts", "oauth2")
add("acct_get_01", "Get the balance and details of an account by account id.", "/v1/accounts/{id}", "GET", "accounts", "oauth2")
add("acct_statement_01", "Retrieve a statement of transactions for an account over a period.", "/v1/accounts/{id}/statement", "GET", "accounts", "oauth2")
add("acct_close_01", "Close an existing account and settle any remaining balance.", "/v1/accounts/{id}", "DELETE", "accounts", "oauth2")

# auth
add("auth_token_01", "Exchange client credentials for an OAuth2 access token.", "/v1/oauth/token", "POST", "auth", "none")
add("auth_revoke_01", "Revoke an issued access or refresh token immediately.", "/v1/oauth/revoke", "POST", "auth", "oauth2")
add("auth_introspect_01", "Introspect a token to check whether it is active and its scopes.", "/v1/oauth/introspect", "POST", "auth", "oauth2")
add("auth_apikey_01", "Create a new API key for server-to-server authentication.", "/v1/apikeys", "POST", "auth", "oauth2")
add("auth_login_legacy", "Legacy username and password login endpoint (deprecated, use OAuth2 token).", "/v1/login", "POST", "auth", "none", status="deprecated")

# customers
add("cust_create_01", "Register a new customer profile with identity and contact details.", "/v1/customers", "POST", "customers", "oauth2")
add("cust_get_01", "Retrieve a customer profile by customer id.", "/v1/customers/{id}", "GET", "customers", "oauth2")
add("cust_update_01", "Update a customer's contact information or profile fields.", "/v1/customers/{id}", "PATCH", "customers", "oauth2")
add("cust_kyc_01", "Submit or check the KYC (know-your-customer) verification status for a customer.", "/v1/customers/{id}/kyc", "POST", "customers", "oauth2")

# notifications
add("notif_send_01", "Send a transactional notification (SMS, email, or push) to a customer.", "/v1/notifications", "POST", "notifications", "oauth2")
add("notif_prefs_01", "Get or update a customer's notification channel preferences.", "/v1/customers/{id}/notifications", "GET", "notifications", "oauth2")
add("notif_webhook_01", "Register a webhook URL to receive event notifications for your application.", "/v1/webhooks", "POST", "notifications", "oauth2")

# transactions
add("txn_transfer_01", "Transfer funds between two accounts within the same institution.", "/v1/transfers", "POST", "transactions", "oauth2")
add("txn_get_01", "Retrieve the details of a single transaction by transaction id.", "/v1/transactions/{id}", "GET", "transactions", "oauth2")
add("txn_list_01", "List transactions for an account filtered by date, type, or amount.", "/v1/transactions", "GET", "transactions", "oauth2")

out = os.path.join(os.path.dirname(__file__) or ".", "dataset", "api_catalog.csv")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id","text","endpoint","method","domain","auth","version","status"])
    w.writeheader(); w.writerows(rows)

print(f"Wrote {len(rows)} API endpoints to {out}")
from collections import Counter
for field in ["domain","method","auth","version","status"]:
    print(f"  {field}:", dict(Counter(r[field] for r in rows)))
