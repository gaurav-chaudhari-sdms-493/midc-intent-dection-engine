import sys
from pathlib import Path
import pytest

# Add the project root directory to the Python path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.ingestion.document_processing.pdf_extractor import extract_pdf_text

def test_extract_pdf_text_from_text_pdf(synthetic_pdf_with_text):
    """Test extraction from a PDF with an extractable text layer."""
    text = extract_pdf_text(synthetic_pdf_with_text)
    assert "This is a sample English text for PDF extraction." in text
    assert "It contains multiple lines to test the extraction." in text
    assert len(text) > 50 # Ensure a reasonable amount of text is extracted

def test_extract_pdf_text_from_scanned_pdf(synthetic_scanned_pdf):
    """Test extraction from a PDF that simulates a scanned document (no text layer)."""
    text = extract_pdf_text(synthetic_scanned_pdf)
    assert text == "" # Expect empty string for scanned PDF
