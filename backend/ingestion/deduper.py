import hashlib
import sys
from pathlib import Path

# Add the parent directory of the current file to the Python path
# to allow importing modules from sibling directories like 'normalizer'.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from normalizer import normalize_text

def content_hash(text: str) -> str:
    """
    Generates an SHA-256 hexadecimal digest of the normalized input text.

    This hash can be used for exact-match deduplication against previously
    seen inquiries. The function is pure and does not involve any I/O or
    storage logic.

    Args:
        text: The input string to be hashed.

    Returns:
        A string representing the SHA-256 hexadecimal digest of the
        normalized text.
    """
    normalized = normalize_text(text)
    # Encode the normalized string to bytes before hashing
    hashed_content = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    return hashed_content

if __name__ == "__main__":
    print("--- Content Hash Examples ---")

    text1 = "  Hello World!  यह एक नमूना हिंदी पाठ है।  \n  TESTING  "
    text2 = "hello world! यह एक नमूना हिंदी पाठ है। testing" # Already normalized version of text1
    text3 = "Another unique piece of text."
    text4 = "  Another unique piece of text.  " # Same as text3 after normalization
    text5 = "  Hello World!  यह एक नमूना हिंदी पाठ है।  \n  TESTING  " # Identical to text1

    hash1 = content_hash(text1)
    hash2 = content_hash(text2)
    hash3 = content_hash(text3)
    hash4 = content_hash(text4)
    hash5 = content_hash(text5)

    print(f"Text 1: '{text1}'")
    print(f"Hash 1: {hash1}")
    print(f"Text 2: '{text2}'")
    print(f"Hash 2: {hash2}")
    print(f"Text 3: '{text3}'")
    print(f"Hash 3: {hash3}")
    print(f"Text 4: '{text4}'")
    print(f"Hash 4: {hash4}")
    print(f"Text 5: '{text5}'")
    print(f"Hash 5: {hash5}")

    print("\n--- Deduplication Check ---")
    print(f"Hash 1 == Hash 2: {hash1 == hash2} (Expected: True)")
    print(f"Hash 1 == Hash 3: {hash1 == hash3} (Expected: False)")
    print(f"Hash 3 == Hash 4: {hash3 == hash4} (Expected: True)")
    print(f"Hash 1 == Hash 5: {hash1 == hash5} (Expected: True)")
