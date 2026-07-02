import sys
from pathlib import Path
import pytest
import logging

# Add the project root directory to the Python path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.ingestion.connectors.chat_transcript import flatten_transcript

# Suppress logging during tests for cleaner output unless explicitly testing logs
@pytest.fixture(autouse=True)
def caplog_fixture(caplog):
    caplog.set_level(logging.WARNING)

def test_flatten_transcript_normal_turns():
    """Test flattening a transcript with normal, well-formed turns."""
    turns = [
        {"speaker": "Customer", "message": "Hello, I have a question."},
        {"speaker": "Agent", "message": "How can I help you today?"},
        {"speaker": "Customer", "message": "My application ID is 123."}
    ]
    expected_output = (
        "Customer: Hello, I have a question.\n"
        "Agent: How can I help you today?\n"
        "Customer: My application ID is 123."
    )
    assert flatten_transcript(turns) == expected_output

def test_flatten_transcript_with_whitespace_in_turns():
    """Test flattening with leading/trailing whitespace in speaker/message."""
    turns = [
        {"speaker": "  User  ", "message": "  Query text.  "},
        {"speaker": "Bot", "message": "Response here.   "}
    ]
    expected_output = (
        "User: Query text.\n"
        "Bot: Response here."
    )
    assert flatten_transcript(turns) == expected_output

def test_flatten_transcript_empty_list():
    """Test flattening an empty list of turns."""
    turns = []
    assert flatten_transcript(turns) == ""

def test_flatten_transcript_malformed_missing_speaker(caplog):
    """Test handling of a malformed turn missing the 'speaker' key."""
    turns = [
        {"speaker": "Customer", "message": "First message."},
        {"message": "Missing speaker."}, # Malformed
        {"speaker": "Agent", "message": "Second message."}
    ]
    expected_output = (
        "Customer: First message.\n"
        "Agent: Second message."
    )
    assert flatten_transcript(turns) == expected_output
    assert "Skipping turn at index 1: 'speaker' key is missing" in caplog.text

def test_flatten_transcript_malformed_missing_message(caplog):
    """Test handling of a malformed turn missing the 'message' key."""
    turns = [
        {"speaker": "Customer", "message": "First message."},
        {"speaker": "Agent"}, # Malformed
        {"speaker": "Customer", "message": "Second message."}
    ]
    expected_output = (
        "Customer: First message.\n"
        "Customer: Second message."
    )
    assert flatten_transcript(turns) == expected_output
    assert "Skipping turn at index 1: 'message' key is missing" in caplog.text

def test_flatten_transcript_malformed_empty_speaker_message(caplog):
    """Test handling of malformed turns with empty speaker or message strings."""
    turns = [
        {"speaker": "Customer", "message": "Valid message."},
        {"speaker": "", "message": "Empty speaker."}, # Malformed
        {"speaker": "Agent", "message": ""}, # Malformed
        {"speaker": "User", "message": "Another valid message."}
    ]
    expected_output = (
        "Customer: Valid message.\n"
        "User: Another valid message."
    )
    assert flatten_transcript(turns) == expected_output
    assert "Skipping turn at index 1: 'speaker' key is missing or not a non-empty string" in caplog.text
    assert "Skipping turn at index 2: 'message' key is missing or not a non-empty string" in caplog.text

def test_flatten_transcript_not_dict_turn(caplog):
    """Test handling of a turn that is not a dictionary."""
    turns = [
        {"speaker": "Customer", "message": "Valid message."},
        "This is not a dict", # Malformed
        {"speaker": "Agent", "message": "Another valid message."}
    ]
    expected_output = (
        "Customer: Valid message.\n"
        "Agent: Another valid message."
    )
    assert flatten_transcript(turns) == expected_output
    assert "Skipping malformed turn at index 1: Expected a dictionary, got str." in caplog.text

def test_flatten_transcript_all_malformed(caplog):
    """Test flattening a list where all turns are malformed."""
    turns = [
        {"speaker": "Customer"},
        "not a dict",
        {"message": "only message"}
    ]
    assert flatten_transcript(turns) == ""
    assert "Skipping turn at index 0: 'message' key is missing" in caplog.text
    assert "Skipping malformed turn at index 1: Expected a dictionary, got str." in caplog.text
    assert "Skipping turn at index 2: 'speaker' key is missing" in caplog.text
