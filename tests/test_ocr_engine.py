import sys
from pathlib import Path
import pytest

# Add the project root directory to the Python path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.ingestion.document_processing.ocr_engine import run_ocr

def test_run_ocr_english(synthetic_image_en):
    """Test OCR on a synthetic English image."""
    text = run_ocr(synthetic_image_en)
    assert "Hello World!" in text
    assert "English text" in text
    assert len(text) > 20

def test_run_ocr_hindi(synthetic_image_hi):
    """Test OCR on a synthetic Hindi image."""
    text = run_ocr(synthetic_image_hi)
    # Check for key Hindi words. OCR might not be perfect, so check for parts.
    assert "नमस्ते" in text or "नमस्" in text
    assert "दुनिया" in text or "दुनि" in text
    assert "हिंदी" in text or "हिं" in text
    assert len(text) > 20

def test_run_ocr_marathi(synthetic_image_mr):
    """Test OCR on a synthetic Marathi image."""
    text = run_ocr(synthetic_image_mr)
    # Check for key Marathi words.
    assert "नमस्कार" in text or "नमस्क" in text
    assert "जग" in text
    assert "मराठीमध्ये" in text or "मराठी" in text
    assert len(text) > 20

def test_run_ocr_empty_bytes():
    """Test OCR with empty image bytes."""
    text = run_ocr(b"")
    assert text == ""

def test_run_ocr_invalid_bytes():
    """Test OCR with invalid image bytes."""
    text = run_ocr(b"this is not an image")
    assert text == ""
