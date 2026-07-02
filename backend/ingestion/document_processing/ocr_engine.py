# Required system packages for Tesseract OCR:
# sudo apt-get install tesseract-ocr tesseract-ocr-hin tesseract-ocr-mar

import pytesseract
from PIL import Image
import io

def run_ocr(image_bytes: bytes) -> str:
    """
    Performs Optical Character Recognition (OCR) on image bytes using pytesseract.

    Supports English, Hindi, and Marathi languages in a single pass.

    Args:
        image_bytes: The content of the image file as bytes.

    Returns:
        A string containing the text extracted from the image.
    """
    try:
        # Convert bytes to a PIL Image object
        image = Image.open(io.BytesIO(image_bytes))

        # Perform OCR using pytesseract with specified languages
        text: str = pytesseract.image_to_string(image, lang="eng+hin+mar")
        return text
    except Exception as e:
        print(f"Error during OCR processing: {e}")
        return ""

if __name__ == "__main__":
    # Example Usage:
    # To test, you would need an image file (e.g., JPG, PNG)
    # and have tesseract-ocr and language packs installed.

    # Example for an English image (replace with actual image path)
    # try:
    #     with open("path/to/your/english_image.png", "rb") as f:
    #         english_image_content = f.read()
    #     english_text = run_ocr(english_image_content)
    #     print("Extracted English Text:")
    #     print(english_text[:500])
    # except FileNotFoundError:
    #     print("English image file not found. Skipping example.")

    # Example for a Hindi/Marathi image (replace with actual image path)
    # try:
    #     with open("path/to/your/hindi_marathi_image.png", "rb") as f:
    #         hindi_marathi_image_content = f.read()
    #     hindi_marathi_text = run_ocr(hindi_marathi_image_content)
    #     print("\nExtracted Hindi/Marathi Text:")
    #     print(hindi_marathi_text[:500])
    # except FileNotFoundError:
    #     print("Hindi/Marathi image file not found. Skipping example.")
    pass
