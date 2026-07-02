import sys
from pathlib import Path
import pytest

# Add the project root directory to the Python path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.ingestion.deduper import content_hash

def test_content_hash_same_input_same_hash():
    """Test that identical inputs produce identical hashes."""
    text1 = "This is a sample text for deduplication."
    text2 = "This is a sample text for deduplication."
    assert content_hash(text1) == content_hash(text2)

def test_content_hash_different_input_different_hash():
    """Test that different inputs produce different hashes."""
    text1 = "This is the first sample text."
    text2 = "This is the second sample text."
    assert content_hash(text1) != content_hash(text2)

def test_content_hash_normalization_effect():
    """Test that normalization affects the hash, making semantically same texts hash to same value."""
    text1 = "  Hello World!  यह एक नमूना हिंदी पाठ है।  \n  TESTING  "
    text2 = "hello world! यह एक नमूना हिंदी पाठ है। testing" # Normalized version of text1
    text3 = "Hello world! यह एक नमूना हिंदी पाठ है। testing" # Same as text2, but with different casing in Latin part
    assert content_hash(text1) == content_hash(text2)
    assert content_hash(text1) == content_hash(text3) # Should be same due to normalization

def test_content_hash_case_sensitivity_latin():
    """Test that Latin casing differences are normalized before hashing."""
    text1 = "Apple"
    text2 = "apple"
    assert content_hash(text1) == content_hash(text2)

def test_content_hash_whitespace_sensitivity():
    """Test that whitespace differences are normalized before hashing."""
    text1 = "text with   multiple    spaces"
    text2 = "text with multiple spaces"
    assert content_hash(text1) == content_hash(text2)

def test_content_hash_control_chars_sensitivity():
    """Test that control characters are removed before hashing."""
    text1 = "text\x01with\x02control\x03chars"
    text2 = "textwithcontrolchars"
    assert content_hash(text1) == content_hash(text2)

def test_content_hash_empty_string():
    """Test hashing an empty string."""
    assert content_hash("") == content_hash("   ") # Empty string and whitespace-only should hash to same

def test_content_hash_devanagari_case_preserved():
    """Test that Devanagari casing (if any) is preserved and doesn't affect hash differently."""
    # Devanagari doesn't typically have case, but ensuring it's not altered by latin lowercasing.
    text1 = "नमस्ते दुनिया!"
    text2 = "नमस्ते दुनिया!"
    assert content_hash(text1) == content_hash(text2)
