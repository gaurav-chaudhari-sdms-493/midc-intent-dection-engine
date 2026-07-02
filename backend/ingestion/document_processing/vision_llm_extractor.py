import os
import base64
from typing import Tuple
import re

# Ensure you have the anthropic package installed: pip install anthropic
from anthropic import Anthropic

def should_use_vision_fallback(ocr_text: str, image_bytes: bytes) -> bool:
    """
    Determines if a vision-based LLM fallback should be used based on OCR output quality.

    This heuristic flags OCR output as unreliable if:
    - The ocr_text is empty.
    - The ocr_text is very short (e.g., less than 50 characters), suggesting minimal text was found.
    - The ocr_text has a high ratio of non-alphanumeric characters (e.g., > 30%),
      indicating potential "garbage" or poor recognition.

    Args:
        ocr_text: The text extracted by the OCR engine.
        image_bytes: The raw bytes of the image (used for context, though not directly
                     in the current heuristic for text quality).

    Returns:
        True if the vision LLM fallback should be used, False otherwise.
    """
    if not ocr_text.strip():
        return True  # OCR returned empty or only whitespace

    # Heuristic 1: Very short text
    if len(ocr_text.strip()) < 50:  # Arbitrary threshold for "very short"
        return True

    # Heuristic 2: High ratio of non-alphanumeric characters
    # Count alphanumeric characters (letters and numbers)
    alphanumeric_chars = sum(c.isalnum() for c in ocr_text)
    total_chars = len(ocr_text)

    if total_chars > 0:
        non_alphanumeric_ratio = (total_chars - alphanumeric_chars) / total_chars
        if non_alphanumeric_ratio > 0.30:  # Arbitrary threshold for "garbage" ratio
            return True

    return False

def extract_with_vision_llm(image_bytes: bytes, media_type: str) -> str:
    """
    Extracts text from an image using Anthropic's Claude 3 Vision API.

    This is intended for handwriting or poor-quality scans where traditional
    OCR might fail or produce unreliable results.

    Args:
        image_bytes: The content of the image file as bytes.
        media_type: The MIME type of the image (e.g., "image/png", "image/jpeg").

    Returns:
        A string containing the extracted text from the image.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = Anthropic(api_key=api_key)

    # Encode image bytes to base64
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    try:
        message = client.messages.create(
            model="claude-3-opus-20240229",  # Or another suitable Claude 3 model like sonnet/haiku
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract all text from this image. Focus on legibility and completeness. If there's any handwriting, transcribe it accurately. Provide the extracted text as plain text without any additional commentary or formatting."
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_base64,
                            },
                        },
                    ],
                }
            ],
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error calling Anthropic Vision API: {e}")
        return ""

if __name__ == "__main__":
    # Example Usage for should_use_vision_fallback:
    print("--- should_use_vision_fallback Examples ---")
    print(f"Empty OCR text: {should_use_vision_fallback('', b'some_image_bytes')}") # Expected: True
    print(f"Short OCR text: {should_use_vision_fallback('Hello', b'some_image_bytes')}") # Expected: True
    print(f"Garbage OCR text: {should_use_vision_fallback('!@#$%^&*()', b'some_image_bytes')}") # Expected: True
    print(f"Good OCR text: {should_use_vision_fallback('This is a reasonably long and clean text from OCR.', b'some_image_bytes')}") # Expected: False
    print(f"Mixed OCR text: {should_use_vision_fallback('This text has some !@#$ garbage but is long enough.', b'some_image_bytes')}") # Expected: True (due to ratio)
    print(f"Long clean OCR text: {should_use_vision_fallback('This is a very long and clean text that should not trigger the fallback heuristic.', b'some_image_bytes')}") # Expected: False

    # Example Usage for extract_with_vision_llm:
    # To run this, you need:
    # 1. An ANTHROPIC_API_KEY set in your environment variables.
    # 2. A sample image file (e.g., "path/to/your/scanned_document.png").

    # print("\n--- extract_with_vision_llm Example ---")
    # try:
    #     # Replace with a real image file and its correct media type
    #     image_file_path = "path/to/your/scanned_document.png"
    #     image_media_type = "image/png" # or "image/jpeg" etc.

    #     if os.path.exists(image_file_path):
    #         with open(image_file_path, "rb") as f:
    #             sample_image_bytes = f.read()

    #         print(f"Calling Vision LLM for {image_file_path}...")
    #         vision_extracted_text = extract_with_vision_llm(sample_image_bytes, image_media_type)
    #         print("Vision LLM Extracted Text:")
    #         print("--------------------")
    #         print(vision_extracted_text[:500]) # Print first 500 chars
    #         print("--------------------")
    #     else:
    #         print(f"Sample image file not found at {image_file_path}. Skipping Vision LLM example.")
    # except ValueError as e:
    #     print(f"Skipping Vision LLM example due to configuration error: {e}")
    # except Exception as e:
    #     print(f"An error occurred during Vision LLM example: {e}")
