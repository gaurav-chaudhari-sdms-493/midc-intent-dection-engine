import re
import unicodedata

def normalize_text(text: str) -> str:
    """
    Normalizes text by collapsing whitespace, stripping control characters,
    and lowercasing only Latin characters. Devanagari script is left untouched.

    Args:
        text: The input string to normalize.

    Returns:
        The normalized string.

    Examples:
        >>> normalize_text("  Hello World!  यह एक नमूना हिंदी पाठ है।  \\n  TESTING  ")
        'hello world! यह एक नमूना हिंदी पाठ है। testing'

        >>> normalize_text("  MiXeD cAsE Latin and हिंदी text.  \\t  ")
        'mixed case latin and हिंदी text.'

        >>> normalize_text("  \x01Control\x02Chars\x03Here\x04  ")
        'controlcharsher'
    """
    # 1. Strip control characters
    # This regex targets common ASCII control characters (0x00-0x1F) and DEL (0x7F),
    # as well as C1 control characters (0x80-0x9F).
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)

    # 2. Lowercase only Latin characters
    # Iterate through characters and lowercase if they are ASCII alphabetic.
    # This preserves casing for non-Latin scripts like Devanagari.
    processed_chars = []
    for char in text:
        # Check if the character is an ASCII letter (a-z, A-Z)
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            processed_chars.append(char.lower())
        else:
            processed_chars.append(char)
    text = "".join(processed_chars)

    # 3. Collapse repeated whitespace to single spaces
    text = re.sub(r'\s+', ' ', text)

    # 4. Strip leading/trailing whitespace
    text = text.strip()

    return text

if __name__ == "__main__":
    # Run doctests
    import doctest
    doctest.testmod()

    # Additional manual tests
    print("\n--- Manual Tests ---")
    test_cases = [
        "  Hello World!  यह एक नमूना हिंदी पाठ है।  \n  TESTING  ",
        "  MiXeD cAsE Latin and हिंदी text.  \t  ",
        "  \x01Control\x02Chars\x03Here\x04  ",
        "Only English text with CAPS.",
        "केवल हिंदी पाठ।",
        "फक्त मराठी मजकूर.",
        "  Leading and trailing spaces.  ",
        "Multiple    spaces   between    words.",
        "No special characters here.",
        "Text with numbers 123 and symbols !@#$",
        "  \t\n  Mixed   whitespace   and   control\x05chars.  "
    ]

    for i, case in enumerate(test_cases):
        normalized = normalize_text(case)
        print(f"Case {i+1}:")
        print(f"  Original: '{case}'")
        print(f"Normalized: '{normalized}'")
        print("-" * 20)
