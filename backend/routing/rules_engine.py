"""
Implements the core routing logic for classified inquiries.
"""
from typing import Dict, Any

# The import path `..classification.confidence_scorer` assumes this file is run
# as part of the `backend` package.
from ..classification.confidence_scorer import needs_human_review

def route(classification: Dict[str, Any]) -> str:
    """
    Determines the routing destination for a classified inquiry.

    The logic is as follows:
    1.  If the inquiry is flagged for human review (due to low confidence or
        high priority) OR if the intent is a 'new_investment_proposal', it is
        immediately routed to 'officer_desk'. New proposals are always high-value.
    2.  If the inquiry is NOT flagged for review AND its intent is a simple,
        informational query ('general_faq' or 'application_status'), it is
        routed for 'auto_response'.
    3.  In all other cases, the function defaults to 'officer_desk'. This is a
        critical safe default. It ensures that any inquiry that isn't explicitly
        and safely handled by an auto-response is seen by a human.

    Args:
        classification: The classification result dictionary.

    Returns:
        A string representing the destination: 'officer_desk' or 'auto_response'.
    """
    # Rule 1: Always route new investment proposals to an officer.
    if classification.get("primary_intent") == "new_investment_proposal":
        return "officer_desk"

    # Rule 2: Route anything needing human review (low confidence/high priority) to an officer.
    if needs_human_review(classification):
        return "officer_desk"

    # Rule 3: If review is not needed, check if it's a simple intent eligible for auto-response.
    if classification.get("primary_intent") in ["general_faq", "application_status"]:
        return "auto_response"

    # Rule 4 (Safe Default): For any other case, default to sending to an officer.
    # This covers high-confidence but complex intents like 'land_allotment' or 'policy_incentive_query'.
    return "officer_desk"
