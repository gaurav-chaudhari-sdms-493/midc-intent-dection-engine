"""
A STUB module for sending notifications to the officer desk.
"""
import logging
from typing import Dict, Any

# Configure basic logging to see output during local testing
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def notify_officer_desk(inquiry_id: str, classification: Dict[str, Any]) -> None:
    """
    Sends a notification to the officer desk for an inquiry needing review.

    This is currently a STUB function. It simulates sending a notification
    by logging the key details to the console.

    Args:
        inquiry_id: The unique identifier for the inquiry.
        classification: The classification result dictionary for the inquiry.
    """
    # TODO: This is a stub for Person C to integrate with the n8n webhook.
    # The actual implementation should:
    # 1. Read the webhook URL from an environment variable (e.g., N8N_OFFICER_WEBHOOK_URL).
    # 2. Construct the JSON payload as specified below.
    # 3. Make an HTTP POST request to the webhook URL.
    # 4. Include error handling for the network request.

    # Expected Webhook Payload Shape:
    # {
    #   "inquiry_id": "a1b2c3d4-...",
    #   "primary_intent": "new_investment_proposal",
    #   "industry": "auto_components_ev",
    #   "priority": "high",
    #   "confidence": 0.95
    # }

    # Log the call so it's visible during local testing
    log_message = (
        f"STUB :: Notifying officer desk for Inquiry ID: {inquiry_id} | "
        f"Priority: {classification.get('priority', 'N/A')} | "
        f"Industry: {classification.get('industry', 'N/A')}"
    )
    logger.info(log_message)

    # In the final version, this function would not return anything,
    # but it might raise an exception if the notification fails.
    return
