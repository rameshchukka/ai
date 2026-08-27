"""
build_dataset.py
================
Builds a deliberately IMPERFECT enterprise knowledge base, so that each Chroma
Studio view reveals a specific, realistic problem you'd hit in production — and
each problem maps to a concrete decision (enrich metadata, re-chunk, split a
collection, add a document, etc.).

The flaws are intentional and labelled in a hidden 'flaw' column (you'd never
have this in real life — it's here so the playbook can check your findings):

  - duplicates:      near-identical docs that bloat retrieval
  - orphan_topic:    a lone doc on a topic nothing else covers (thin coverage)
  - mislabeled:      metadata 'category' disagrees with the actual text
  - overlong:        a doc that crams 3 unrelated topics together (bad chunking)
  - missing_meta:    docs with no 'category' at all
  - collision:       two docs that SHOULD be distinct but read almost the same

Output: dataset/support_kb.csv  (id, text, category, product, flaw)
"""
import csv, os

rows = []

def add(id, text, category, product, flaw=""):
    rows.append({"id": id, "text": text, "category": category, "product": product, "flaw": flaw})

# --- Clean, well-formed core docs (the "good" baseline) -------------------
add("refund_01", "Refunds are issued within 5 business days to the original payment method once the returned item is received.", "billing", "payments")
add("refund_02", "To request a refund, open a ticket with your order number and reason; approved refunds post in 5 business days.", "billing", "payments")
add("ship_01", "Standard shipping takes 3 to 5 business days. Express shipping is delivered the next business day.", "shipping", "logistics")
add("ship_02", "Orders placed before 2 PM ship the same day. Tracking numbers are emailed once the carrier scans the parcel.", "shipping", "logistics")
add("warranty_01", "The standard warranty covers manufacturing defects for 12 months from the purchase date.", "warranty", "hardware")
add("warranty_02", "Warranty claims require the original receipt and a description of the defect submitted through the support portal.", "warranty", "hardware")
add("auth_01", "API authentication uses OAuth2 bearer tokens. Tokens expire after 60 minutes and must be refreshed.", "api", "platform")
add("auth_02", "To rotate an API key, generate a new key in the console, update your client, then revoke the old key.", "api", "platform")
add("ratelimit_01", "The default API rate limit is 100 requests per minute per key. Exceeding it returns HTTP 429.", "api", "platform")
add("password_01", "To reset your password, use the 'Forgot password' link; a reset email is valid for 30 minutes.", "account", "platform")
add("password_02", "Passwords must be at least 12 characters and include a number and a symbol.", "account", "platform")
add("billing_cycle_01", "Subscriptions renew monthly on the date of initial signup. Invoices are emailed the same day.", "billing", "payments")

# --- FLAW 1: near-duplicates (should be deduped or merged) -----------------
add("refund_03", "Refunds go back to your original payment method within five business days after we receive the returned item.", "billing", "payments", "duplicates")
add("refund_04", "Once the returned product reaches us, your refund is processed to the original payment method within 5 business days.", "billing", "payments", "duplicates")

# --- FLAW 2: orphan topic (thin coverage — only ONE doc mentions it) -------
add("gdpr_01", "Under GDPR, users may request deletion of their personal data; we complete verified deletion requests within 30 days.", "compliance", "platform", "orphan_topic")

# --- FLAW 3: mislabeled metadata (category says 'shipping', text is billing) 
add("mislabel_01", "Late fees of 1.5 percent per month apply to overdue invoices that remain unpaid after 30 days.", "shipping", "payments", "mislabeled")

# --- FLAW 4: overlong doc cramming 3 unrelated topics (bad chunking) -------
add("mixed_01",
    "Our office is open 9 to 5 on weekdays. Separately, the mobile app supports biometric login on iOS and Android. "
    "Also, bulk export of your data is available in CSV and JSON from the account settings page under 'Data'.",
    "misc", "platform", "overlong")

# --- FLAW 5: missing metadata (no category) -------------------------------
add("nometa_01", "Gift cards never expire and can be applied to any order at checkout.", "", "payments", "missing_meta")
add("nometa_02", "Referral credits are added to your account within 24 hours of your friend's first purchase.", "", "payments", "missing_meta")

# --- FLAW 6: semantic collision (two DIFFERENT policies that read alike) ---
add("collision_01", "You can cancel your subscription at any time; access continues until the end of the current billing period.", "billing", "payments", "collision")
add("collision_02", "You can cancel an order any time before it ships; access to the item ends immediately once cancelled.", "shipping", "logistics", "collision")

os.makedirs(os.path.dirname(__file__) + "/dataset", exist_ok=True) if os.path.dirname(__file__) else None
out = os.path.join(os.path.dirname(__file__) or ".", "dataset", "support_kb.csv")
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "text", "category", "product", "flaw"])
    w.writeheader()
    w.writerows(rows)

print(f"Wrote {len(rows)} rows to {out}")
print("Flaw distribution:")
from collections import Counter
for flaw, n in Counter(r["flaw"] or "clean" for r in rows).most_common():
    print(f"  {flaw}: {n}")
