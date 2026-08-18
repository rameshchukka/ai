"""
approval_flow.py
Week 16 - Part B, Step 2: Simulated human-in-the-loop approval

Simulates the approval step that a real high-stakes tool (issue_refund)
requires before anything actually happens. In a real system this would be a
dashboard notification, a Slack approval button, or similar - here it's a
simple CLI prompt so you can exercise the full flow: agent proposes ->
human reviews -> human approves/denies -> agent confirms outcome.

Run: python approval_flow.py
"""

from agent import run_agent
from tools import TOOLS, IssueRefundInput


def request_human_approval(order_id: str, amount: float, reason: str) -> bool:
    """
    Shows the pending refund to a human and asks for approve/deny. Returns
    True if approved. This is the ONLY place a refund can actually be
    marked as issued - the agent itself never has this authority.
    """
    print("\n" + "=" * 60)
    print("APPROVAL REQUIRED")
    print("=" * 60)
    print(f"  Order:  {order_id}")
    print(f"  Amount: ${amount:.2f}")
    print(f"  Reason: {reason}")
    print("=" * 60)

    decision = input("Approve this refund? [y/n]: ").strip().lower()
    return decision == "y"


def finalize_refund(order_id: str, amount: float, approved: bool) -> dict:
    if approved:
        return {"status": "REFUND ISSUED", "order_id": order_id, "amount": amount}
    return {"status": "REFUND DENIED", "order_id": order_id, "amount": amount}


def run_agent_with_approval_gate(task: str) -> str:
    """
    Runs the agent normally. If the agent's final answer recommends issuing
    a refund (per the pattern in mock_responses.py / a real agent's output),
    this wrapper pauses for human approval before considering the task done.

    In a fuller production implementation, the approval gate would live
    INSIDE the agent loop itself (intercepting the issue_refund tool call
    directly, before it ever "executes"). This simplified version approves
    after the agent's recommendation instead, which is easier to follow for
    a first pass - see the TODO below for the more realistic version.
    """
    result = run_agent(task, verbose=True)

    if "propose the refund" in result.lower() or "issue_refund" in result.lower():
        # TODO (stretch goal): parse the actual order_id/amount out of the
        # agent's reasoning instead of hardcoding them here - this simulation
        # keeps it simple since the mock scenario always proposes the same
        # refund, but a real implementation needs to extract these from the
        # agent's tool-call history, not from parsing its final text answer.
        approved = request_human_approval(order_id="ord_1001", amount=49.99, reason="Damaged on arrival")
        outcome = finalize_refund("ord_1001", 49.99, approved)
        print(f"\nOutcome: {outcome}")
        return f"{result}\n\nApproval outcome: {outcome}"

    return result


if __name__ == "__main__":
    task = (
        "A customer says their laptop stand from order ord_1001 arrived damaged. "
        "Look up the order, check refund eligibility, and tell me what should happen next."
    )
    final = run_agent_with_approval_gate(task)
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(final)
