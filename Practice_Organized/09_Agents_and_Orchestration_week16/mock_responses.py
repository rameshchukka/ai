"""
mock_responses.py (Week 16 version - agent-aware)
Unlike Week 14/15's keyword-matching mock, this one is SEQUENCE-based: it
counts how many "Observation:" entries are already in the scratchpad (i.e.
how many loop iterations have happened) to decide which scripted JSON action
to return next. This lets LLM_PROVIDER=mock simulate a full multi-step agent
run deterministically, with no API calls at all.

If you write a new test task in agent.py that isn't recognized below, mock
mode falls back to a generic single-step response - add a new scripted
sequence here if you want richer mock coverage for your own scenario.
"""

import json


def _iteration_depth(user_prompt: str) -> int:
    """How many tool calls have already happened in this run, based on how
    many Observation entries are in the scratchpad so far."""
    return user_prompt.count("Observation:")


def _extract_task_line(user_prompt: str) -> str:
    """
    Only the first line ('Task: ...') should be used for scenario matching -
    NOT the full scratchpad. Tool observations can legitimately contain
    words like 'damaged' or an order ID, which would otherwise cause a later
    iteration to accidentally match the wrong scripted scenario. This bug
    was caught by actually running the max-iteration guard test - a good
    example of why testing your mock data matters as much as testing real
    model calls.
    """
    first_line = user_prompt.split("\n", 1)[0]
    return first_line.replace("Task:", "", 1).strip()


def get_mock_response(system: str, user: str) -> str:
    depth = _iteration_depth(user)
    task_only = _extract_task_line(user)
    lowered_task = task_only.lower()

    # --- Scripted sequence for Test 1: single-tool lookup ---------------
    if "cust_001" in task_only and "look up the account" in lowered_task:
        if depth == 0:
            return json.dumps({
                "thought": "I need to look up this customer's account details.",
                "action": "lookup_customer_account",
                "action_input": {"customer_id": "cust_001"},
            })
        else:
            return json.dumps({
                "thought": "I have the account details, ready to answer.",
                "action": "final_answer",
                "answer": "Customer cust_001 is Priya Sharma (priya@example.com), standard tier.",
            })

    # --- Scripted sequence for Test 2: multi-tool refund eligibility check ---
    if "ord_1001" in task_only and "damaged" in lowered_task:
        if depth == 0:
            return json.dumps({
                "thought": "First, let me check the order details.",
                "action": "check_order_status",
                "action_input": {"order_id": "ord_1001"},
            })
        elif depth == 1:
            return json.dumps({
                "thought": "Order confirms damage was reported. Now checking refund eligibility.",
                "action": "check_refund_eligibility",
                "action_input": {"order_id": "ord_1001"},
            })
        else:
            return json.dumps({
                "thought": "I have enough information to answer.",
                "action": "final_answer",
                "answer": (
                    "Order ord_1001 (Laptop Stand, $49.99) was reported damaged on arrival. "
                    "It's eligible for a refund regardless of the standard 14-day window. "
                    "Next step: propose the refund via issue_refund for human approval."
                ),
            })

    # --- Scripted sequence for a deliberately-never-ending task (tests the guard) ---
    if "loop forever" in lowered_task or "impossible task" in lowered_task:
        # Always proposes another tool call, never a final_answer - this is
        # intentional, to let you observe the max-iteration guard triggering.
        return json.dumps({
            "thought": "I need more information before I can answer.",
            "action": "check_order_status",
            "action_input": {"order_id": "ord_1001"},
        })

    # --- Generic fallback: answer immediately with whatever's known -------
    return json.dumps({
        "thought": "No specific mock script matched this task - answering directly.",
        "action": "final_answer",
        "answer": (
            "[MOCK MODE] No scripted sequence matches this task. Add one to "
            "mock_responses.py's get_mock_response(), or switch LLM_PROVIDER to "
            "'gemini_auto' to get a real agent run."
        ),
    })
