"""
Provides a function to determine if a classification result requires human review.
"""
from typing import Dict, Any

def needs_human_review(classification: Dict[str, Any], threshold: float = 0.6) -> bool:
    """
    Determines if an inquiry's classification warrants human review.

    A review is triggered if the model's confidence is below the threshold,
    or, critically, if the inquiry is classified as 'high' priority. This
    ensures that potentially high-value or urgent inquiries (like a major
    investment proposal) are always seen by a human, regardless of how
    confident the model is in its classification.

    Args:
        classification: The classification result dictionary, expected to
                        contain 'priority' and 'confidence' keys.
        threshold: The confidence score below which a review is triggered.

    Returns:
        True if the classification needs human review, False otherwise.
    """
    # Business Rule: All high-priority inquiries must be reviewed by a human
    # to ensure accuracy and appropriate handling. This is a critical safeguard.
    if classification.get("priority") == "high":
        return True

    # If not high-priority, then check if confidence is below the threshold.
    # Default to 1.0 (no review) if confidence key is missing.
    if classification.get("confidence", 1.0) < threshold:
        return True

    return False
