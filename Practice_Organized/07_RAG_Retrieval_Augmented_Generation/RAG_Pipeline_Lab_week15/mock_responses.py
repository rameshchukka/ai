"""
mock_responses.py
Pre-written, realistic mock responses used when LLM_PROVIDER=mock.

This lets every exercise script run without a real API key or any network
call — useful for practicing the parsing/logic side of each exercise, or for
working through the lab before your Gemini key is set up.

How it works: get_mock_response() does simple keyword matching against the
incoming user message to decide which canned response to return. It's not
meant to be clever - it's meant to be predictable, so you know exactly what
you're testing against.
"""

import random

# --- Exercise 1: temperature -------------------------------------------------
TAGLINE_RESPONSES = [
    "Wake up. Brew up. Show up.",
    "Where every cup tells a story.",
    "Coffee that gets you.",
    "Small shop, big flavor.",
    "Your daily dose of good.",
]

# --- Exercise 2: classifier ---------------------------------------------------
CLASSIFIER_KEYWORDS = {
    "crash": "Bug",
    "freeze": "Bug",
    "bulk-delete": "Feature Request",
    "bulk delete": "Feature Request",
    "add dark mode": "Feature Request",
    "dark mode": "Feature Request",
    "how do i": "Question",
    "billing email": "Question",
    "showing up": "Bug",
}

# --- Exercise 3: chain-of-thought ---------------------------------------------
COT_MOCK_DIRECT = "$90 prorated charge. (mock response - not verified math)"
COT_MOCK_REASONED = (
    "Step 1: The customer is on a $120/month plan, billed on the 1st.\n"
    "Step 2: They upgrade to $300/month on the 15th, so 16 days remain in a 30-day month.\n"
    "Step 3: The daily rate difference is ($300 - $120) / 30 = $6/day.\n"
    "Step 4: Prorated charge = $6/day * 16 days = $96.\n"
    "Answer: $96 (mock response - verify this math yourself, don't trust it blindly)"
)

# --- Exercise 4: structured output --------------------------------------------
CLEAN_JSON_RESPONSE = (
    '{"company_name": "Acme Robotics Inc.", "contract_value": "$480,000", '
    '"renewal_date": "January 15, 2027", "risk_flags": ["auto-renewal clause", '
    '"minimum order volume requirement"]}'
)

MESSY_JSON_RESPONSE = (
    "Sure, here's the extracted contract data:\n\n"
    "```json\n"
    '{"company_name": "Acme Robotics Inc.", "contract_value": "$480,000", '
    '"renewal_date": "January 15, 2027", "risk_flags": ["auto-renewal clause"]}\n'
    "```\n\n"
    "Let me know if you need anything else!"
)

# A genuinely broken one, on purpose - for testing your parser's failure path
BROKEN_JSON_RESPONSE = (
    '{"company_name": "Acme Robotics Inc.", "contract_value": "$480,000", '
    '"renewal_date": "January 15, 2027", "risk_flags": ["auto-renewal clause",}'  # trailing comma, invalid
)

# --- Exercise 5: context management -------------------------------------------
MOCK_SUMMARIES = {
    "refund": "Full refund within 14 days if unopened; store credit only after that, "
              "up to 30 days; digital goods non-refundable after download.",
    "shipping": "Standard shipping: 5-7 days. Express (+$12): 1-2 days, domestic only. "
                "International: up to 21 days, no express option.",
    "warranty": "1-year warranty on manufacturing defects, not accidental damage. "
                "Extended warranty (up to 3 years) purchasable within 30 days of purchase.",
}

MOCK_SYNTHESIS_ANSWER = (
    "Based on the policies: (1) The customer is within the 14-day refund window, so a "
    "full refund is possible. (2) Express shipping is NOT available for international "
    "orders, so the replacement would ship via standard international shipping "
    "(up to 21 business days). (3) Since they are within 30 days of purchase, they CAN "
    "still add a 3-year extended warranty.\n\n"
    "(mock response - cross-check this against the real policy text yourself)"
)

# --- Real-world use case: triage ------------------------------------------
TRIAGE_MOCK_RESPONSES = {
    "charged twice": (
        '{"urgency": "HIGH", "customer_name": "Priya", "product_area": "Billing", '
        '"sentiment": "negative", "suggested_first_response": '
        '"Hi Priya, I\'m sorry for the frustration. Let me look into the duplicate '
        'charge on your account right away and follow up shortly."}'
    ),
    "dark mode": (
        '{"urgency": "LOW", "customer_name": "", "product_area": "Mobile App", '
        '"sentiment": "neutral", "suggested_first_response": '
        '"Thanks for the suggestion! Dark mode isn\'t available yet, but I\'ve logged '
        'this as a feature request for our product team."}'
    ),
    "production integration down": (
        '{"urgency": "HIGH", "customer_name": "James", "product_area": "Integrations", '
        '"sentiment": "negative", "suggested_first_response": '
        '"Hi James, thank you for flagging this immediately. I\'m escalating this to '
        'our on-call engineering team right now and will update you within the hour."}'
    ),
}


def get_mock_response(system: str, user: str) -> str:
    """
    Simple keyword-based mock response selector. Returns a realistic-looking
    response string based on what's in the user message - good enough to
    exercise your parsing/handling code without a live API call.
    """
    lowered_user = user.lower()
    lowered_system = system.lower()

    # Exercise 1: tagline requests
    if "tagline" in lowered_user or "coffee shop" in lowered_user:
        return random.choice(TAGLINE_RESPONSES)

    # Exercise 2: classifier
    if "classify" in lowered_system and ("bug" in lowered_system or "feature request" in lowered_system):
        for keyword, label in CLASSIFIER_KEYWORDS.items():
            if keyword in lowered_user:
                return label
        return "Question"  # default fallback

    # Exercise 3: chain-of-thought
    if "prorated" in lowered_user or "renewal date" in lowered_user:
        if "step by step" in lowered_system or "show your reasoning" in lowered_system:
            return COT_MOCK_REASONED
        return COT_MOCK_DIRECT

    # Exercise 4: structured output
    if "acme robotics" in lowered_user:
        if "brief one-sentence explanation" in lowered_system:
            return MESSY_JSON_RESPONSE
        return CLEAN_JSON_RESPONSE

    # Exercise 5: context management
    if "refund policy" in lowered_user:
        return MOCK_SUMMARIES["refund"]
    if "shipping policy" in lowered_user:
        return MOCK_SUMMARIES["shipping"]
    if "warranty policy" in lowered_user:
        return MOCK_SUMMARIES["warranty"]
    if "germany" in lowered_user and "express" in lowered_user:
        return MOCK_SYNTHESIS_ANSWER

    # Real-world use case: triage
    for keyword, response in TRIAGE_MOCK_RESPONSES.items():
        if keyword in lowered_user:
            return response

    # Default fallback for anything unmatched
    return (
        "[MOCK MODE] No canned response matches this prompt. Add a new entry to "
        "mock_responses.py, or switch LLM_PROVIDER to 'gemini' in your .env to get "
        "a real model response."
    )
