import sys
from pathlib import Path
import pytest

# Add the project root directory to the Python path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.ingestion.normalizer import normalize_text

def test_normalize_text_whitespace_collapse():
    """Test collapsing of repeated whitespace to single spaces."""
    text = "This   has    too  much   whitespace."
    expected = "this has too much whitespace."
    assert normalize_text(text) == expected

def test_normalize_text_leading_trailing_whitespace():
    """Test stripping of leading and trailing whitespace."""
    text = "  \t  Hello World!   \n  "
    expected = "hello world!"
    assert normalize_text(text) == expected

def test_normalize_text_control_chars_strip():
    """Test stripping of control characters."""
    text = "Text\x01with\x02control\x03chars\x04."
    expected = "textwithcontrolchars."
    assert normalize_text(text) == expected

def test_normalize_text_devanagari_case_preserved():
    """Test that Devanagari script case is preserved (i.e., not lowercased)."""
    text = "यह एक नमूना हिंदी पाठ है। MiXeD cAsE."
    expected = "यह एक नमूना हिंदी पाठ है। mixed case."
    assert normalize_text(text) == expected

def test_normalize_text_mixed_latin_devanagari():
    """Test mixed Latin and Devanagari with various normalization aspects."""
    text = "  MiXeD   cAsE   Latin   and   यह   एक   नमूना   हिंदी   पाठ   है।   \t  "
    expected = "mixed case latin and यह एक नमूना हिंदी पाठ है।"
    assert normalize_text(text) == expected

def test_normalize_text_empty_string():
    """Test with an empty string."""
    assert normalize_text("") == ""

def test_normalize_text_only_whitespace():
    """Test with only whitespace."""
    assert normalize_text("   \n\t  ") == ""

def test_normalize_text_only_control_chars():
    """Test with only control characters."""
    text = "\x01\x02\x03"
    assert normalize_text(text) == ""

def test_normalize_text_numbers_and_symbols():
    """Test with numbers and symbols, ensuring they are preserved."""
    text = "123 Test!@#$ %^&*()"
    expected = "123 test!@#$ %^&*()"
    assert normalize_text(text) == expected
