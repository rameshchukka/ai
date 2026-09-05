"""
build_dataset.py — a small, hand-labeled corpus for learning RAG foundations.
Small enough to verify every number by hand; rich enough to show real behavior.

Outputs:
  dataset/corpus.csv   — 24 short "knowledge base" documents with a topic label
  dataset/queries.csv  — 10 labeled queries -> the doc ids that are truly relevant
"""
import csv, os

docs = []
def d(id, text, topic):
    docs.append({"id": id, "text": text, "topic": topic})

# --- payments / billing ---
d("d01","You can request a refund within 30 days of purchase for a full return.","refunds")
d("d02","Refunds are processed back to your original payment method in 5 business days.","refunds")
d("d03","To get your money back, open a refund request from the orders page.","refunds")
d("d04","We accept Visa, Mastercard, and American Express credit cards.","payment")
d("d05","You can pay using PayPal or a bank transfer at checkout.","payment")
d("d06","Subscriptions renew automatically each month on your billing date.","payment")
# --- shipping ---
d("d07","Standard shipping takes three to five business days to arrive.","shipping")
d("d08","Express delivery arrives the next business day for an extra fee.","shipping")
d("d09","We ship internationally, but customs can add one to two weeks.","shipping")
d("d10","Track your package using the tracking number in your confirmation email.","shipping")
# --- account ---
d("d11","Reset your password using the forgot-password link on the sign-in page.","account")
d("d12","You can change your email address in the account settings page.","account")
d("d13","To delete your account, contact support and confirm by email.","account")
d("d14","Enable two-factor authentication for extra account security.","account")
# --- product / clothing (a second domain, like the course's Fashion Hub) ---
d("d15","This jacket is waterproof and windproof, ideal for winter hiking.","product")
d("d16","Our running shoes are lightweight with breathable mesh uppers.","product")
d("d17","The wool sweater is machine washable on a gentle cold cycle.","product")
d("d18","These sunglasses block one hundred percent of UVA and UVB rays.","product")
d("d19","The backpack has a padded laptop sleeve and water-bottle pockets.","product")
d("d20","This t-shirt is made from organic cotton and comes in five colors.","product")
# --- support / warranty ---
d("d21","All products include a one-year limited warranty against defects.","warranty")
d("d22","Contact customer support by chat or email seven days a week.","support")
d("d23","Damaged items can be exchanged free of charge within 14 days.","warranty")
d("d24","Our help center has step-by-step guides and video tutorials.","support")

out = os.path.join(os.path.dirname(__file__) or ".", "corpus.csv")
with open(out,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["id","text","topic"]); w.writeheader(); w.writerows(docs)
print(f"wrote {len(docs)} docs -> {out}")

# labeled queries (ground truth). intent-based relevance, hand-checkable.
queries = []
def q(qid, text, rel):
    queries.append({"qid":qid,"query":text,"relevant_ids":" ".join(rel)})

q("q1","how do I get a refund",["d01","d02","d03"])
q("q2","what credit cards can I use to pay",["d04","d05"])
q("q3","how long does delivery take",["d07","d08","d09"])
q("q4","I forgot my password",["d11"])
q("q5","how do I track my order",["d10"])
q("q6","waterproof jacket for hiking",["d15"])
q("q7","tell me about the warranty",["d21","d23"])
q("q8","how can I contact support",["d22","d24"])
q("q9","organic cotton clothing",["d20","d17"])
q("q10","cancel my subscription billing",["d06"])

outq = os.path.join(os.path.dirname(__file__) or ".", "queries.csv")
with open(outq,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["qid","query","relevant_ids"]); w.writeheader(); w.writerows(queries)
print(f"wrote {len(queries)} queries -> {outq}")
