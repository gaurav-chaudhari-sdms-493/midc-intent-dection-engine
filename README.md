# MIDC Investor Inquiry Ingestion Pipeline

This module provides a standalone Python 3.11 pipeline for ingesting investor inquiries from various channels (email, portal, chat), processing them, and producing a clean, normalized output matching a defined contract. This output is intended to be consumed by a downstream classification module.

## 1. Output Contract

The `process_inquiry()` function in `backend/ingestion/pipeline.py` produces a dictionary with the following exact JSON shape:

```json
{
  "inquiry_id": "uuid",
  "channel": "email | portal | chat",
  "original_text": "string",
  "original_language": "en | hi | mr",
  "normalized_text": "string",
  "translated_text": "string (English canonical, optional)"
}
```

**Details:**
*   `inquiry_id`: A unique UUID (string format) generated for each inquiry.
*   `channel`: The source channel of the inquiry.
*   `original_text`: The raw, combined text content of the inquiry before any normalization or translation.
*   `original_language`: The detected language of the `original_text` ("en", "hi", or "mr").
*   `normalized_text`: The `original_text` after whitespace collapse, control character stripping, and lowercasing of only Latin characters (Devanagari script case is preserved).
*   `translated_text`: The `original_text` translated to English. This field is **optional** and will only be present if `original_language` is not "en". If `original_language` is "en", the `normalized_text` serves as the English canonical form.

## 2. Setup Instructions

### Python Environment
This module requires **Python 3.11**.

1.  **Create and activate a virtual environment:**
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    The `requirements.txt` file contains:
    ```
    fasttext
    PyMuPDF
    pytesseract
    Pillow
    anthropic
    requests
    imap-tools
    reportlab
    ```

### OS-level Tesseract Setup
For Optical Character Recognition (OCR) capabilities, you need to install Tesseract OCR and its language packs for Hindi and Marathi.

On Debian/Ubuntu-based systems:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-hin tesseract-ocr-mar
```
For other operating systems, please refer to the Tesseract documentation for installation instructions.

### fastText Language Model
The `backend/ingestion/language/lang_detect.py` module uses the `lid.176.bin` fastText language identification model.

1.  **Download the model:**
    Download `lid.176.bin` from: [https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin)

2.  **Place the model:**
    Create a `models` directory inside `backend/ingestion/language/` and place the downloaded `lid.176.bin` file there.
    Example path: `/home/stark/PycharmProjects/midc-intent-dection-engine/backend/ingestion/language/models/lid.176.bin`

3.  **Gitignore:**
    It is highly recommended to add `backend/ingestion/language/models/lid.176.bin` to your `.gitignore` file to avoid committing large binary files to your repository.

## 3. Required Environment Variables

The pipeline relies on several environment variables for API keys and service credentials. These should be set in your environment (e.g., in a `.env` file loaded by a tool like `python-dotenv`).

*   `BHASHINI_API_KEY`: API key for the Bhashini translation service.
*   `ANTHROPIC_API_KEY`: API key for Anthropic's Claude 3 Vision API (used for advanced image text extraction).
*   `IMAP_HOST`: IMAP server hostname for fetching emails.
*   `IMAP_USER`: Username for IMAP server authentication.
*   `IMAP_PASSWORD`: Password for IMAP server authentication.

## 4. Known Limitations / TODOs

*   **IndicTrans2 Fallback**: The `backend/ingestion/language/translator.py` module includes a stub for a self-hosted IndicTrans2 translation model, but it is not yet implemented or integrated into the `translate_to_english` function. Currently, Bhashini is the primary (and only active) translation path.
*   **Scanned PDF Rasterization**: In `backend/ingestion/pipeline.py`, when a PDF has no extractable text layer, the current implementation rasterizes only the *first page* to an image for OCR/Vision LLM processing. A more robust solution for multi-page scanned PDFs would involve rasterizing all relevant pages.
*   **Bhashini Endpoint Schema**: The HTTP call to the Bhashini API in `backend/ingestion/language/translator.py` is currently stubbed with a placeholder endpoint and payload. The exact endpoint URL and request/response schema need to be confirmed and implemented once the official Bhashini API documentation is available.

## 5. Minimal Usage Example

To use the `process_inquiry` function, ensure your environment variables are set and all setup steps are completed.

```python
import os
from backend.ingestion.pipeline import process_inquiry
from backend.ingestion.connectors.email_connector import fetch_new_emails # Example for email

# --- Example 1: Text-only inquiry (Portal Channel) ---
print("--- Processing Portal Inquiry (English Text) ---")
portal_text = "I need information about industrial land allocation in Pune."
try:
    result_portal = process_inquiry(channel="portal", text=portal_text)
    print(result_portal)
except ValueError as e:
    print(f"Error processing portal inquiry: {e}")

# --- Example 2: Chat Transcript Inquiry (Chat Channel) ---
print("\n--- Processing Chat Inquiry (Hindi Turns) ---")
chat_turns = [
    {"speaker": "ग्राहक", "message": "नमस्ते, मुझे एक प्रश्न है।"},
    {"speaker": "एजेंट", "message": "कृपया अपना प्रश्न बताएं।"}
]
try:
    # Note: This will attempt to call the (stubbed) Bhashini API for translation
    result_chat = process_inquiry(channel="chat", text=chat_turns)
    print(result_chat)
except ValueError as e:
    print(f"Error processing chat inquiry: {e}")

# --- Example 3: File-based Inquiry (simulated PDF with text) ---
# For a real test, you would load actual file bytes.
# Using a synthetic PDF for demonstration.
from tests.conftest import synthetic_pdf_with_text # Assuming conftest is accessible

print("\n--- Processing File Inquiry (Synthetic PDF) ---")
try:
    # This fixture needs to be called as a function to get the bytes
    # In a real application, you'd read from a file:
    # with open("path/to/your/document.pdf", "rb") as f:
    #     pdf_bytes = f.read()
    
    # For this example, we'll use the fixture directly.
    # Note: synthetic_pdf_with_text is a fixture, so it's usually passed to a test function.
    # For a direct script, we'd need to generate it or load a pre-existing one.
    # Let's simulate loading from a pre-existing file for this example.
    
    # To run this example, ensure 'tests/fixtures/synthetic_text.pdf' exists
    # (it's generated by running pytest or the test_week1.py script once).
    pdf_file_path = Path(__file__).parent / "tests" / "fixtures" / "synthetic_text.pdf"
    if pdf_file_path.exists():
        with open(pdf_file_path, "rb") as f:
            pdf_bytes_for_example = f.read()
        
        result_file = process_inquiry(
            channel="email",
            file_bytes=pdf_bytes_for_example,
            file_type="application/pdf"
        )
        print(result_file)
    else:
        print(f"Skipping PDF example: {pdf_file_path} not found. Run tests/test_pipeline.py once to generate fixtures.")
except ValueError as e:
    print(f"Error processing file inquiry: {e}")

# --- Example 4: Fetching and processing new emails (requires IMAP env vars) ---
# print("\n--- Fetching and Processing New Emails ---")
# try:
#     new_emails = fetch_new_emails()
#     if new_emails:
#         for i, email_data in enumerate(new_emails):
#             print(f"\nProcessing Email {i+1}:")
#             email_result = process_inquiry(
#                 channel="email",
#                 text=email_data["text"],
#                 # For emails, attachments would need separate handling if they contain primary content
#                 # file_bytes=email_data["attachments"][0] if email_data["attachments"] else None,
#                 # file_type="image/png" # or other detected type
#             )
#             print(email_result)
#     else:
#         print("No new emails to process.")
# except Exception as e:
#     print(f"Error fetching/processing emails: {e}")
```
