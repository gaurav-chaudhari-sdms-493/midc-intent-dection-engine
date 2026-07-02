import sys
from pathlib import Path
import pytest
from unittest.mock import MagicMock, patch
import os

# Add the project root directory to the Python path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.ingestion.pipeline import process_inquiry
from backend.ingestion.language.lang_detect import _model # To mock fasttext model if needed

# --- Mocks for external dependencies ---

@pytest.fixture(autouse=True)
def mock_external_dependencies(monkeypatch):
    # Mock fastText model for language detection
    class MockFastTextModel:
        def predict(self, text, k=1):
            if "english" in text.lower() or "hello" in text.lower() or "test" in text.lower() or "sample" in text.lower() or "query" in text.lower() or "vision llm" in text.lower() or "ocr extracted" in text.lower():
                return (['__label__en'], [0.9])
            elif "hindi" in text.lower() or "नमस्ते" in text or "हिंदी" in text or "ग्राहक" in text or "एजेंट" in text:
                return (['__label__hi'], [0.9])
            elif "marathi" in text.lower() or "नमस्कार" in text or "मराठी" in text:
                return (['__label__mr'], [0.9])
            else: # Fallback for gibberish or unknown
                return (['__label__en'], [0.4]) # Low confidence to trigger fallback

    monkeypatch.setattr("backend.ingestion.language.lang_detect._model", MockFastTextModel())

    # Mock Anthropic client for vision LLM
    mock_anthropic_client = MagicMock()
    mock_anthropic_client.messages.create.return_value.content = [MagicMock(text="Vision LLM extracted text")]
    monkeypatch.setattr("backend.ingestion.document_processing.vision_llm_extractor.Anthropic", MagicMock(return_value=mock_anthropic_client))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "dummy_anthropic_key")

    # Mock requests for Bhashini API
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None # No HTTP errors
    # Mock the actual structure of the Bhashini API response for translation
    mock_response.json.return_value = {"pipelineResponse": [{"output": [{"target": "Translated to English"}]}]}
    monkeypatch.setattr("requests.post", MagicMock(return_value=mock_response))
    monkeypatch.setenv("BHASHINI_API_KEY", "dummy_bhashini_key")

    # Mock IMAP for email_connector (though not directly used in pipeline.py, good practice)
    monkeypatch.setenv("IMAP_HOST", "dummy_host")
    monkeypatch.setenv("IMAP_USER", "dummy_user")
    monkeypatch.setenv("IMAP_PASSWORD", "dummy_password")


# --- Tests for process_inquiry ---

def test_process_inquiry_text_only_english_email():
    """Test processing an English text-only inquiry from email channel."""
    text = "This is an English test inquiry for email."
    result = process_inquiry(channel="email", text=text)

    assert result["channel"] == "email"
    assert result["original_text"] == text
    assert result["original_language"] == "en"
    assert result["normalized_text"] == "this is an english test inquiry for email."
    assert "translated_text" not in result # Should not be present if original is English
    assert isinstance(result["inquiry_id"], str)
    assert len(result["inquiry_id"]) == 36 # UUID length

def test_process_inquiry_text_only_hindi_portal():
    """Test processing a Hindi text-only inquiry from portal channel."""
    text = "यह एक हिंदी परीक्षण पूछताछ है।" # "This is a Hindi test inquiry."
    result = process_inquiry(channel="portal", text=text)

    assert result["channel"] == "portal"
    assert result["original_text"] == text
    assert result["original_language"] == "hi"
    assert result["normalized_text"] == "यह एक हिंदी परीक्षण पूछताछ है।" # Devanagari not lowercased
    assert result["translated_text"] == "Translated to English" # Mocked translation
    assert isinstance(result["inquiry_id"], str)

def test_process_inquiry_chat_turns_english():
    """Test processing chat turns in English."""
    chat_turns = [
        {"speaker": "Customer", "message": "Hello, I have a query."},
        {"speaker": "Agent", "message": "How can I assist you?"}
    ]
    result = process_inquiry(channel="chat", text=chat_turns)

    assert result["channel"] == "chat"
    assert result["original_text"] == "Customer: Hello, I have a query.\nAgent: How can I assist you?"
    assert result["original_language"] == "en"
    assert result["normalized_text"] == "customer: hello, i have a query. agent: how can i assist you?"
    assert "translated_text" not in result

def test_process_inquiry_chat_turns_hindi():
    """Test processing chat turns in Hindi."""
    chat_turns = [
        {"speaker": "ग्राहक", "message": "नमस्ते, मुझे एक प्रश्न है।"},
        {"speaker": "एजेंट", "message": "मैं आपकी कैसे मदद कर सकता हूँ?"}
    ]
    result = process_inquiry(channel="chat", text=chat_turns)

    assert result["channel"] == "chat"
    assert result["original_text"] == "ग्राहक: नमस्ते, मुझे एक प्रश्न है।\nएजेंट: मैं आपकी कैसे मदद कर सकता हूँ?"
    assert result["original_language"] == "hi"
    assert result["normalized_text"] == "ग्राहक: नमस्ते, मुझे एक प्रश्न है। एजेंट: मैं आपकी कैसे मदद कर सकता हूँ?"
    assert result["translated_text"] == "Translated to English"

def test_process_inquiry_file_pdf_with_text(synthetic_pdf_with_text):
    """Test processing a PDF with an extractable text layer."""
    result = process_inquiry(channel="portal", file_bytes=synthetic_pdf_with_text, file_type="application/pdf")

    assert result["channel"] == "portal"
    assert "sample English text" in result["original_text"]
    assert result["original_language"] == "en"
    assert "sample english text" in result["normalized_text"]
    assert "translated_text" not in result

def test_process_inquiry_file_scanned_pdf_triggers_ocr_vision_llm(synthetic_scanned_pdf, monkeypatch):
    """
    Test processing a scanned PDF, which should trigger the OCR path and then
    the Vision LLM fallback due to empty OCR result.
    """
    # Mock run_ocr to return empty string for scanned PDF
    monkeypatch.setattr("backend.ingestion.document_processing.ocr_engine.run_ocr", MagicMock(return_value=""))
    # Mock extract_with_vision_llm to return a specific text
    mock_vision_llm_extractor = MagicMock(return_value="Vision LLM extracted text from scanned PDF.")
    monkeypatch.setattr("backend.ingestion.document_processing.vision_llm_extractor.extract_with_vision_llm", mock_vision_llm_extractor)

    result = process_inquiry(channel="email", file_bytes=synthetic_scanned_pdf, file_type="application/pdf")

    assert result["channel"] == "email"
    assert "Vision LLM extracted text from scanned PDF." in result["original_text"]
    assert result["original_language"] == "en" # Vision LLM output is English
    assert "vision llm extracted text from scanned pdf." in result["normalized_text"]
    assert "translated_text" not in result
    mock_vision_llm_extractor.assert_called_once() # Ensure Vision LLM was called

def test_process_inquiry_file_image_triggers_ocr(synthetic_image_en, monkeypatch):
    """Test processing an image file, triggering OCR."""
    # Mock run_ocr to return a specific text for the image
    mock_ocr_runner = MagicMock(return_value="OCR extracted text from image.")
    monkeypatch.setattr("backend.ingestion.document_processing.ocr_engine.run_ocr", mock_ocr_runner)
    # Ensure vision fallback is NOT triggered
    monkeypatch.setattr("backend.ingestion.document_processing.vision_llm_extractor.should_use_vision_fallback", MagicMock(return_value=False))

    result = process_inquiry(channel="portal", file_bytes=synthetic_image_en, file_type="image/png")

    assert result["channel"] == "portal"
    assert "OCR extracted text from image." in result["original_text"]
    assert result["original_language"] == "en"
    assert "ocr extracted text from image." in result["normalized_text"]
    assert "translated_text" not in result
    mock_ocr_runner.assert_called_once()

def test_process_inquiry_file_image_triggers_vision_fallback(synthetic_image_hi, monkeypatch):
    """Test processing an image file where OCR is unreliable, triggering Vision LLM."""
    # Mock run_ocr to return a short, unreliable string
    mock_ocr_runner = MagicMock(return_value="!@#$")
    monkeypatch.setattr("backend.ingestion.document_processing.ocr_engine.run_ocr", mock_ocr_runner)
    # Mock should_use_vision_fallback to return True
    monkeypatch.setattr("backend.ingestion.document_processing.vision_llm_extractor.should_use_vision_fallback", MagicMock(return_value=True))
    # Mock extract_with_vision_llm to return a specific text
    mock_vision_llm_extractor = MagicMock(return_value="Vision LLM extracted text from Hindi image.")
    monkeypatch.setattr("backend.ingestion.document_processing.vision_llm_extractor.extract_with_vision_llm", mock_vision_llm_extractor)

    result = process_inquiry(channel="portal", file_bytes=synthetic_image_hi, file_type="image/png")

    assert result["channel"] == "portal"
    assert "Vision LLM extracted text from Hindi image." in result["original_text"]
    assert result["original_language"] == "en" # Vision LLM output is English
    assert "vision llm extracted text from hindi image." in result["normalized_text"]
    assert "translated_text" not in result # Vision LLM output is already English
    mock_ocr_runner.assert_called_once()
    mock_vision_llm_extractor.assert_called_once()

def test_process_inquiry_value_error_no_input():
    """Test that ValueError is raised if neither text nor file_bytes is provided."""
    with pytest.raises(ValueError, match="Either 'text' or 'file_bytes' must be provided."):
        process_inquiry(channel="portal")

def test_process_inquiry_value_error_empty_processed_text(monkeypatch):
    """Test that ValueError is raised if processed text content ends up empty."""
    # Mock all extractors to return empty strings
    monkeypatch.setattr("backend.ingestion.document_processing.pdf_extractor.extract_pdf_text", MagicMock(return_value=""))
    monkeypatch.setattr("backend.ingestion.document_processing.ocr_engine.run_ocr", MagicMock(return_value=""))
    monkeypatch.setattr("backend.ingestion.document_processing.vision_llm_extractor.extract_with_vision_llm", MagicMock(return_value=""))
    monkeypatch.setattr("backend.ingestion.connectors.chat_transcript.flatten_transcript", MagicMock(return_value=""))

    with pytest.raises(ValueError, match="No meaningful text content could be extracted or provided for processing."):
        process_inquiry(channel="portal", text="   ", file_bytes=b"dummy", file_type="image/png")

def test_process_inquiry_combines_text_and_file_content(synthetic_pdf_with_text):
    """Test that text and file content are combined correctly."""
    text_input = "Additional text from the user."
    result = process_inquiry(channel="email", text=text_input, file_bytes=synthetic_pdf_with_text, file_type="application/pdf")

    assert "Additional text from the user." in result["original_text"]
    assert "sample English text" in result["original_text"]
    assert "\n\n" in result["original_text"] # Check for separator
    assert result["original_language"] == "en"
    assert "additional text from the user. sample english text" in result["normalized_text"]
    assert "translated_text" not in result

def test_process_inquiry_combines_chat_and_file_content(synthetic_pdf_with_text):
    """Test that chat turns and file content are combined correctly."""
    chat_turns = [
        {"speaker": "User", "message": "Chat message."},
    ]
    result = process_inquiry(channel="chat", text=chat_turns, file_bytes=synthetic_pdf_with_text, file_type="application/pdf")

    assert "User: Chat message." in result["original_text"]
    assert "sample English text" in result["original_text"]
    assert "\n\n" in result["original_text"] # Check for separator
    assert result["original_language"] == "en"
    assert "user: chat message. sample english text" in result["normalized_text"]
    assert "translated_text" not in result
