from typing import List, Dict, Any
import logging

# Configure logging for this module
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def flatten_transcript(turns: List[Dict[str, str]]) -> str:
    """
    Flattens a list of chat turn dictionaries into a single readable text block.

    Each turn dictionary is expected to have at least "speaker" and "message" keys.
    The function joins these turns, preserving their original order, into a format
    like "Speaker: Message". Missing or malformed turn dictionaries are skipped
    with a warning, preventing crashes.

    Args:
        turns: A list of dictionaries, where each dictionary represents a chat turn
               and is expected to contain "speaker" and "message" keys.

    Returns:
        A single string representing the flattened chat transcript.
    """
    flattened_lines: List[str] = []
    for i, turn in enumerate(turns):
        if not isinstance(turn, dict):
            logger.warning(f"Skipping malformed turn at index {i}: Expected a dictionary, got {type(turn).__name__}.")
            continue

        speaker = turn.get("speaker")
        message = turn.get("message")

        if not isinstance(speaker, str) or not speaker.strip():
            logger.warning(f"Skipping turn at index {i}: 'speaker' key is missing or not a non-empty string. Turn: {turn}")
            continue
        if not isinstance(message, str) or not message.strip():
            logger.warning(f"Skipping turn at index {i}: 'message' key is missing or not a non-empty string. Turn: {turn}")
            continue

        flattened_lines.append(f"{speaker.strip()}: {message.strip()}")

    return "\n".join(flattened_lines)

if __name__ == "__main__":
    print("--- Flatten Transcript Examples ---")

    # Example 1: Valid turns
    valid_transcript = [
        {"speaker": "Customer", "message": "Hello, I have an inquiry about my application."},
        {"speaker": "Agent", "message": "Certainly, I can help you with that. What is your application ID?"},
        {"speaker": "Customer", "message": "It's MIDC-2023-001."},
        {"speaker": "Agent", "message": "Thank you. Let me check that for you."}
    ]
    print("Valid Transcript:")
    print(flatten_transcript(valid_transcript))
    print("-" * 30)

    # Example 2: Transcript with missing keys and malformed turns
    malformed_transcript = [
        {"speaker": "Customer", "message": "I need help."},
        {"speaker": "Agent"}, # Missing message
        {"message": "What's the issue?"}, # Missing speaker
        "This is not a dict", # Not a dict
        {"speaker": "Customer", "message": ""}, # Empty message
        {"speaker": "Agent", "message": "I'm here to assist."},
        {"speaker": "", "message": "Empty speaker name."}, # Empty speaker
    ]
    print("\nMalformed Transcript (warnings expected):")
    print(flatten_transcript(malformed_transcript))
    print("-" * 30)

    # Example 3: Empty transcript
    empty_transcript: List[Dict[str, str]] = []
    print("\nEmpty Transcript:")
    print(f"'{flatten_transcript(empty_transcript)}'")
    print("-" * 30)

    # Example 4: Transcript with leading/trailing whitespace
    whitespace_transcript = [
        {"speaker": "  User  ", "message": "  My query.  "},
        {"speaker": "  Bot  ", "message": "  Here is the answer.  "}
    ]
    print("\nWhitespace Transcript:")
    print(flatten_transcript(whitespace_transcript))
    print("-" * 30)
