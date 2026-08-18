"""
mock_data.py
Week 16 - Part A, Step 1: Mock data

A small fake customer/order database - real Python dicts, no real service
needed. Every tool in tools.py reads from (or, for refunds, only proposes
changes to) this data.
"""

CUSTOMERS = {
    "cust_001": {"name": "Priya Sharma", "email": "priya@example.com", "tier": "standard"},
    "cust_002": {"name": "James Okoye", "email": "james@example.com", "tier": "enterprise"},
    "cust_003": {"name": "Maria Lopez", "email": "maria@example.com", "tier": "standard"},
}

ORDERS = {
    "ord_1001": {
        "customer_id": "cust_001",
        "item": "Laptop Stand",
        "amount": 49.99,
        "purchase_date": "2026-07-27",  # 9 days before "today" (2026-08-05) for testing
        "status": "delivered",
        "condition_reported": "damaged on arrival",
    },
    "ord_1002": {
        "customer_id": "cust_002",
        "item": "Replacement Cable",
        "amount": 12.50,
        "purchase_date": "2026-08-01",
        "status": "processing",
        "condition_reported": None,
    },
    "ord_1003": {
        "customer_id": "cust_003",
        "item": "Extended Warranty - Monitor",
        "amount": 49.00,
        "purchase_date": "2026-06-01",  # over 30 days ago - outside extended warranty window
        "status": "delivered",
        "condition_reported": None,
    },
}

# Ticket "database" - create_support_ticket appends here
SUPPORT_TICKETS = []


def get_customer(customer_id: str) -> dict:
    return CUSTOMERS.get(customer_id)


def get_order(order_id: str) -> dict:
    return ORDERS.get(order_id)
