"""
tools.py
Week 16 - Part A, Step 1: Tool definitions

Each tool is a real Python function with a docstring (used to build the
agent's system prompt) and a Pydantic model describing its input schema
(used to validate the agent's proposed arguments before we execute anything).

Part A tools: lookup_customer_account, check_order_status, create_support_ticket
Part B adds: check_refund_eligibility (RAG-grounded), issue_refund (never
auto-executes - see approval_flow.py)
"""

from pydantic import BaseModel, Field
from mock_data import get_customer, get_order, SUPPORT_TICKETS


# --- Input schemas -----------------------------------------------------------

class LookupCustomerInput(BaseModel):
    customer_id: str = Field(..., description="The customer ID, e.g. 'cust_001'")


class CheckOrderStatusInput(BaseModel):
    order_id: str = Field(..., description="The order ID, e.g. 'ord_1001'")


class CreateSupportTicketInput(BaseModel):
    customer_id: str = Field(..., description="The customer ID this ticket is for")
    issue: str = Field(..., description="A short description of the issue")


class CheckRefundEligibilityInput(BaseModel):
    order_id: str = Field(..., description="The order ID to check refund eligibility for")


class IssueRefundInput(BaseModel):
    order_id: str = Field(..., description="The order ID to refund")
    amount: float = Field(..., description="The refund amount in dollars")
    reason: str = Field(..., description="Why this refund is being proposed")


# --- Tool functions ------------------------------------------------------------

def lookup_customer_account(customer_id: str) -> dict:
    """Look up a customer's account details (name, email, tier) by customer ID."""
    customer = get_customer(customer_id)
    if customer is None:
        return {"error": f"No customer found with ID '{customer_id}'"}
    return {"customer_id": customer_id, **customer}


def check_order_status(order_id: str) -> dict:
    """Look up an order's status, item, amount, purchase date, and any reported condition issues."""
    order = get_order(order_id)
    if order is None:
        return {"error": f"No order found with ID '{order_id}'"}
    return {"order_id": order_id, **order}


def create_support_ticket(customer_id: str, issue: str) -> dict:
    """Create a support ticket for a customer describing an issue. Returns the new ticket ID."""
    ticket_id = f"tkt_{len(SUPPORT_TICKETS) + 1:04d}"
    ticket = {"ticket_id": ticket_id, "customer_id": customer_id, "issue": issue, "status": "open"}
    SUPPORT_TICKETS.append(ticket)
    return ticket


def check_refund_eligibility(order_id: str) -> dict:
    """
    Check whether an order is eligible for a refund per policy. In Part A,
    this uses simple hardcoded rules as a placeholder. In Part B, replace
    the body of this function to call Week 15's RAG pipeline instead (see
    integrated_eligibility.py) so eligibility is grounded in the real policy
    documents rather than rules duplicated here.
    """
    order = get_order(order_id)
    if order is None:
        return {"error": f"No order found with ID '{order_id}'"}

    if order.get("condition_reported") == "damaged on arrival":
        return {"eligible": True, "reason": "Damaged item - eligible for refund regardless of the 14-day window."}

    # Simplified 14-day rule for Part A placeholder purposes only
    return {
        "eligible": None,
        "reason": (
            "Part A placeholder: cannot determine standard-window eligibility without "
            "real date math and real policy grounding - see Part B's RAG-grounded version."
        ),
    }


def issue_refund(order_id: str, amount: float, reason: str) -> dict:
    """
    Propose a refund for an order. This NEVER executes automatically - it
    always returns a 'pending_approval' status. A human must approve it via
    approval_flow.py before anything is actually marked as refunded.
    """
    return {
        "status": "pending_approval",
        "order_id": order_id,
        "amount": amount,
        "reason": reason,
        "note": "This refund has NOT been issued. It requires human approval - run approval_flow.py.",
    }


# --- Tool registry, used by agent.py to build the system prompt and dispatch calls ---

TOOLS = {
    "lookup_customer_account": {
        "function": lookup_customer_account,
        "input_model": LookupCustomerInput,
        "description": lookup_customer_account.__doc__.strip(),
    },
    "check_order_status": {
        "function": check_order_status,
        "input_model": CheckOrderStatusInput,
        "description": check_order_status.__doc__.strip(),
    },
    "create_support_ticket": {
        "function": create_support_ticket,
        "input_model": CreateSupportTicketInput,
        "description": create_support_ticket.__doc__.strip(),
    },
    "check_refund_eligibility": {
        "function": check_refund_eligibility,
        "input_model": CheckRefundEligibilityInput,
        "description": check_refund_eligibility.__doc__.strip(),
    },
    "issue_refund": {
        "function": issue_refund,
        "input_model": IssueRefundInput,
        "description": issue_refund.__doc__.strip(),
    },
}
