import sys
from pathlib import Path
import pytest

# Add the project root directory to the Python path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.ingestion.language.lang_detect import detect_language, _CONFIDENCE_THRESHOLD

# Mock the fastText model if it's not available or for specific test cases
# This is important because the model loading happens at module level.
# For testing, we might want to control its behavior.
# However, for now, we'll assume the model is correctly loaded as per instructions.

def test_detect_language_english():
    """Test language detection for English text."""
    text = "This is a sample English sentence."
    assert detect_language(text) == "en"

def test_detect_language_hindi():
    """Test language detection for Hindi text."""
    text = "यह एक नमूना हिंदी वाक्य है।"
    assert detect_language(text) == "hi"

def test_detect_language_marathi():
    """Test language detection for Marathi text."""
    text = "हे एक नमुना मराठी वाक्य आहे."
    assert detect_language(text) == "mr"

def test_detect_language_mixed_english_hindi():
    """Test language detection for mixed English and Hindi text (should lean towards dominant)."""
    text = "Hello, यह एक नमूना हिंदी वाक्य है।"
    # FastText might pick up Hindi or English depending on the model and text length.
    # For this test, we'll accept either if the model is good, but default to 'en' if it's ambiguous.
    # Given the current model, it often picks the first dominant language or 'en' as fallback.
    # Let's assume it should ideally pick 'hi' if Hindi is dominant, or 'en' if mixed.
    # For now, we'll check if it's one of the expected.
    detected = detect_language(text)
    assert detected in ["en", "hi"] # Depending on model's sensitivity

def test_detect_language_low_confidence_gibberish():
    """Test language detection for gibberish or low-confidence text, expecting fallback to 'en'."""
    text = "asdfghjkl zxcvbnm qwert"
    assert detect_language(text) == "en"

def test_detect_language_empty_string():
    """Test language detection for an empty string, expecting fallback to 'en'."""
    assert detect_language("") == "en"

def test_detect_language_whitespace_only():
    """Test language detection for whitespace-only string, expecting fallback to 'en'."""
    assert detect_language("   \n\t  ") == "en"

# To properly test the _CONFIDENCE_THRESHOLD, we would need to mock fasttext.load_model
# and its predict method to return specific confidence scores.
# For now, we rely on the gibberish test to implicitly cover low confidence.
# Example of how you might mock it (not executed here):
# @pytest.fixture
# def mock_fasttext_low_confidence(monkeypatch):
#     class MockModel:
#         def predict(self, text, k=1):
#             return (['__label__fr'], [0.4]) # Simulate low confidence French
#     monkeypatch.setattr("fasttext.load_model", lambda x: MockModel())
#     monkeypatch.setattr("backend.ingestion.language.lang_detect._model", MockModel())
#
# def test_detect_language_mocked_low_confidence(mock_fasttext_low_confidence):
#     assert detect_language("some french text") == "en"
