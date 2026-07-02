import sys
from pathlib import Path
import pytest
import uuid

# Add the project root directory to the Python path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.ingestion.pipeline import process_inquiry

# The mock_external_dependencies fixture from conftest.py will automatically
# mock fastText, Anthropic, and Bhashini APIs, ensuring these tests run fast
# and don't require actual API keys or models.

def test_contract_shape_english_input():
    """
    Tests the contract shape for process_inquiry output with English text input.
    Ensures all keys are present and types are correct, and translated_text is absent.
    """
    sample_text = "This is a sample inquiry in English."
    output = process_inquiry(channel="portal", text=sample_text)

    # 1. Check for all 6 keys
    expected_keys = {
        "inquiry_id",
        "channel",
        "original_text",
        "original_language",
        "normalized_text",
        # "translated_text" is optional and should be absent for English
    }
    assert set(output.keys()) == expected_keys, f"Missing or extra keys. Expected {expected_keys}, got {output.keys()}"

    # 2. Check types and values
    assert isinstance(output["inquiry_id"], str)
    assert isinstance(output["channel"], str)
    assert isinstance(output["original_text"], str)
    assert isinstance(output["original_language"], str)
    assert isinstance(output["normalized_text"], str)

    # 3. Specific value checks
    assert uuid.UUID(output["inquiry_id"], version=4) # Check if it's a valid UUID v4
    assert output["channel"] == "portal"
    assert output["original_language"] == "en"
    assert output["original_text"] == sample_text
    assert "translated_text" not in output # Should not be present for English source

def test_contract_shape_hindi_input():
    """
    Tests the contract shape for process_inquiry output with Hindi text input.
    Ensures all keys are present and types are correct, and translated_text is present.
    """
    sample_text = "यह एक नमूना हिंदी पूछताछ है।" # "This is a sample Hindi inquiry."
    output = process_inquiry(channel="email", text=sample_text)

    # 1. Check for all 6 keys (including translated_text)
    expected_keys = {
        "inquiry_id",
        "channel",
        "original_text",
        "original_language",
        "normalized_text",
        "translated_text", # Should be present for non-English source
    }
    assert set(output.keys()) == expected_keys, f"Missing or extra keys. Expected {expected_keys}, got {output.keys()}"

    # 2. Check types and values
    assert isinstance(output["inquiry_id"], str)
    assert isinstance(output["channel"], str)
    assert isinstance(output["original_text"], str)
    assert isinstance(output["original_language"], str)
    assert isinstance(output["normalized_text"], str)
    assert isinstance(output["translated_text"], str) # Should be a string

    # 3. Specific value checks
    assert uuid.UUID(output["inquiry_id"], version=4) # Check if it's a valid UUID v4
    assert output["channel"] == "email"
    assert output["original_language"] == "hi"
    assert output["original_text"] == sample_text
    assert output["translated_text"] == "Translated to English" # From mock

def test_contract_shape_marathi_input():
    """
    Tests the contract shape for process_inquiry output with Marathi text input.
    Ensures all keys are present and types are correct, and translated_text is present.
    """
    sample_text = "हे एक नमुना मराठी चौकशी आहे." # "This is a sample Marathi inquiry."
    output = process_inquiry(channel="chat", text=sample_text)

    # 1. Check for all 6 keys (including translated_text)
    expected_keys = {
        "inquiry_id",
        "channel",
        "original_text",
        "original_language",
        "normalized_text",
        "translated_text", # Should be present for non-English source
    }
    assert set(output.keys()) == expected_keys, f"Missing or extra keys. Expected {expected_keys}, got {output.keys()}"

    # 2. Check types and values
    assert isinstance(output["inquiry_id"], str)
    assert isinstance(output["channel"], str)
    assert isinstance(output["original_text"], str)
    assert isinstance(output["original_language"], str)
    assert isinstance(output["normalized_text"], str)
    assert isinstance(output["translated_text"], str) # Should be a string

    # 3. Specific value checks
    assert uuid.UUID(output["inquiry_id"], version=4) # Check if it's a valid UUID v4
    assert output["channel"] == "chat"
    assert output["original_language"] == "mr"
    assert output["original_text"] == sample_text
    assert output["translated_text"] == "Translated to English" # From mock
