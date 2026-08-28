"""
build_dataset.py
================
Builds a small support knowledge base with RICH, MULTI-FIELD metadata so you can
test that metadata ingestion and filtering work end to end in Chroma Studio.

Each row has FOUR metadata fields you can filter/summarize on:
  - topic     (cooking / finance / shipping / api / account)
  - type      (core / near_duplicate / edge_case)
  - product   (payments / logistics / platform / hardware)
  - priority  (high / medium / low)

Multiple fields let you test single-field filters AND combinations.

Output: dataset/support_docs.csv  (id, text, topic, type, product, priority)
"""
import csv, os

rows = []
def add(id, text, topic, type_, product, priority):
    rows.append({"id": id, "text": text, "topic": topic, "type": type_,
                 "product": product, "priority": priority})

# cooking
add("cook_01", "Sauteing vegetables over high heat caramelizes their natural sugars quickly.", "cooking", "core", "platform", "low")
add("cook_02", "A classic French baguette relies on long fermentation for its open crumb.", "cooking", "core", "platform", "low")
add("cook_03", "Cooking vegetables fast on high heat browns the sugars inside them.", "cooking", "near_duplicate", "platform", "low")

# finance / billing
add("fin_01", "Refunds are processed within 5 business days to the original payment method.", "finance", "core", "payments", "high")
add("fin_02", "To request a refund, open a ticket with your order number and reason.", "finance", "core", "payments", "high")
add("fin_03", "Refunds go back to the original payment method within five business days.", "finance", "near_duplicate", "payments", "high")
add("fin_04", "Subscriptions renew monthly on the signup date; invoices are emailed same day.", "finance", "core", "payments", "medium")

# shipping
add("ship_01", "Standard shipping takes 3 to 5 business days; express is next business day.", "shipping", "core", "logistics", "medium")
add("ship_02", "Orders placed before 2 PM ship the same day.", "shipping", "core", "logistics", "medium")
add("ship_03", "International shipping can take 10 to 20 business days depending on customs.", "shipping", "edge_case", "logistics", "low")

# api
add("api_01", "API authentication uses OAuth2 bearer tokens that expire after 60 minutes.", "api", "core", "platform", "high")
add("api_02", "The default API rate limit is 100 requests per minute per key.", "api", "core", "platform", "high")
add("api_03", "To rotate an API key, generate a new key, update your client, then revoke the old key.", "api", "core", "platform", "medium")

# account
add("acct_01", "To reset your password, use the 'Forgot password' link; the email is valid for 30 minutes.", "account", "core", "platform", "medium")
add("acct_02", "Passwords must be at least 12 characters and include a number and a symbol.", "account", "core", "platform", "low")
add("acct_03", "Enterprise SSO via SAML is available on the Business plan and above only.", "account", "edge_case", "platform", "low")

out = os.path.join(os.path.dirname(__file__) or ".", "dataset", "support_docs.csv")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "text", "topic", "type", "product", "priority"])
    w.writeheader()
    w.writerows(rows)

print(f"Wrote {len(rows)} rows to {out}")
from collections import Counter
for field in ["topic", "type", "product", "priority"]:
    print(f"  {field}:", dict(Counter(r[field] for r in rows)))
