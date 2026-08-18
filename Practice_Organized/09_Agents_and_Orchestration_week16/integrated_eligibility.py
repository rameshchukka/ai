"""
integrated_eligibility.py
Week 16 - Part B, Step 3: Ground eligibility checks in Week 15's RAG pipeline

Replaces Part A's hardcoded check_refund_eligibility() with a version that
actually queries the real policy documents (via Week 15's generate.py) to
determine eligibility, instead of duplicating policy rules as code.

Run: python ingest.py            (once, to build the vector index - reuses
                                   the same docs/ folder from Week 15)
Run: python integrated_eligibility.py

This demonstrates the pattern from the Week 16 tutorial: instead of
hardcoding "damaged items are always eligible" as a Python if-statement
(Part A's approach), the agent's tool now asks the actual policy document
the same way a human support agent would look it up.
"""

from generate import answer_question
from mock_data import get_order


def check_refund_eligibility_grounded(order_id: str) -> dict:
    """
    RAG-grounded version of check_refund_eligibility. Builds a natural-
    language question from the order's actual details and retrieves the
    real policy answer, instead of hardcoded rules.
    """
    order = get_order(order_id)
    if order is None:
        return {"error": f"No order found with ID '{order_id}'"}

    condition = order.get("condition_reported")
    purchase_date = order.get("purchase_date")
    item = order.get("item")

    if condition:
        question = (
            f"A customer bought '{item}' on {purchase_date} and reports the following "
            f"condition issue: '{condition}'. Are they eligible for a refund, and why?"
        )
    else:
        question = (
            f"A customer bought '{item}' on {purchase_date} with no reported condition "
            f"issues. Are they still within the standard refund window? What are their options?"
        )

    rag_result = answer_question(question, top_k=3)

    return {
        "order_id": order_id,
        "eligibility_question_asked": question,
        "policy_answer": rag_result["answer"],
        "grounded_in_sources": rag_result["sources_retrieved"],
    }


if __name__ == "__main__":
    test_orders = ["ord_1001", "ord_1002", "ord_1003"]

    for order_id in test_orders:
        print("=" * 60)
        print(f"Order: {order_id}")
        print("=" * 60)
        result = check_refund_eligibility_grounded(order_id)
        for key, value in result.items():
            print(f"{key}: {value}")
        print()

    print(
        "Compare these answers against Part A's hardcoded check_refund_eligibility() "
        "in tools.py - note how ord_1002 (no condition issue, recent purchase) and "
        "ord_1003 (extended warranty, purchased over 30 days ago) get real, specific "
        "policy-grounded answers here instead of Part A's 'cannot determine' placeholder."
    )
