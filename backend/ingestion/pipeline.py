import uuid
import sys
from pathlib import Path
from typing import Dict, List, Any, Union

# Add the project root directory to the Python path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import all necessary modules
from ingestion.document_processing.pdf_extractor import extract_pdf_text
from ingestion.document_processing.ocr_engine import run_ocr
from ingestion.document_processing.vision_llm_extractor import should_use_vision_fallback, extract_with_vision_llm
from ingestion.connectors.chat_transcript import flatten_transcript
from ingestion.language.lang_detect import detect_language
from ingestion.normalizer import normalize_text
from ingestion.language.translator import translate_to_english
from ingestion.deduper import content_hash

# For PDF rasterization (if a scanned PDF needs OCR)
import fitz # PyMuPDF

def process_inquiry(
    channel: str,
    text: Union[str, List[Dict[str, str]], None] = None,
    file_bytes: bytes | None = None,
    file_type: str | None = None
) -> Dict[str, str]:
    """
    Orchestrates the data ingestion pipeline for an investor inquiry.

    Processes an inquiry from various channels (email, portal, chat) which
    can include text, file attachments (PDF, images). It extracts text,
    detects language, normalizes, translates, and generates a content hash.

    Args:
        channel: The source channel of the inquiry ("email", "portal", "chat").
        text: Optional. The raw text content of the inquiry. For "chat" channel,
              this can also be a list of dictionaries representing chat turns.
        file_bytes: Optional. The raw bytes of an attached file.
        file_type: Optional. The MIME type of the attached file (e.g., "application/pdf",
                   "image/png", "image/jpeg").

    Returns:
        A dictionary matching the specified contract:
        {
          "inquiry_id": "uuid",
          "channel": "email | portal | chat",
          "original_text": "string",
          "original_language": "en | hi | mr",
          "normalized_text": "string",
          "translated_text": "string (English canonical, optional)"
        }

    Raises:
        ValueError: If neither text nor file_bytes is provided, or if the
                    processed text content ends up being empty.
    """
    combined_raw_text_content = ""
    extracted_file_text = ""
    processed_file_bytes_for_ocr = file_bytes # Bytes that might be passed to OCR/Vision LLM
    processed_file_type_for_ocr = file_type   # Type for processed_file_bytes_for_ocr

    if not text and not file_bytes:
        raise ValueError("Either 'text' or 'file_bytes' must be provided.")

    # 1. File Processing
    if file_bytes and file_type:
        if file_type == "application/pdf":
            extracted_pdf_text = extract_pdf_text(file_bytes)
            if extracted_pdf_text:
                extracted_file_text = extracted_pdf_text
            else:
                # PDF has no extractable text layer, treat as scanned.
                # TODO: For multi-page PDFs, a more robust approach would be needed
                # to rasterize all pages or select the most relevant one.
                # For now, we'll rasterize the first page to PNG for OCR/Vision LLM.
                print("PDF has no text layer. Attempting to rasterize first page for OCR/Vision LLM.")
                try:
                    pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
                    if pdf_document.page_count > 0:
                        page = pdf_document.load_page(0) # Load first page
                        # Render at 2x resolution for better OCR quality
                        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                        processed_file_bytes_for_ocr = pix.tobytes(format="png")
                        processed_file_type_for_ocr = "image/png"
                        print("Rasterized PDF first page to PNG image bytes.")
                    else:
                        print("PDF has no pages to rasterize for OCR/Vision LLM.")
                        processed_file_bytes_for_ocr = None
                        processed_file_type_for_ocr = None
                    pdf_document.close()
                except Exception as e:
                    print(f"Error rasterizing PDF for OCR/Vision LLM fallback: {e}")
                    processed_file_bytes_for_ocr = None
                    processed_file_type_for_ocr = None

        # If processed_file_bytes_for_ocr is now an image (either original image or rasterized PDF)
        if processed_file_bytes_for_ocr and processed_file_type_for_ocr and processed_file_type_for_ocr.startswith("image/"):
            print(f"Processing image file (type: {processed_file_type_for_ocr}).")
            ocr_result = run_ocr(processed_file_bytes_for_ocr)
            if should_use_vision_fallback(ocr_result, processed_file_bytes_for_ocr):
                print("OCR result deemed unreliable. Falling back to Vision LLM.")
                extracted_file_text = extract_with_vision_llm(processed_file_bytes_for_ocr, processed_file_type_for_ocr)
            else:
                extracted_file_text = ocr_result
            print(f"Extracted text from file (first 100 chars): {extracted_file_text[:100]}...")

    # Combine extracted file text with provided text
    # This will be the 'original_text' in the output contract
    if extracted_file_text and text:
        # If text is a list of turns, it will be flattened.
        if isinstance(text, list):
            combined_raw_text_content = f"{extracted_file_text}\n\n{flatten_transcript(text)}"
        else:
            combined_raw_text_content = f"{extracted_file_text}\n\n{text}"
    elif extracted_file_text:
        combined_raw_text_content = extracted_file_text
    elif text:
        if isinstance(text, list):
            combined_raw_text_content = flatten_transcript(text)
        else:
            combined_raw_text_content = text

    if not combined_raw_text_content.strip():
        raise ValueError("No meaningful text content could be extracted or provided for processing.")

    final_original_text = combined_raw_text_content

    # 3. detect_language()
    original_language = detect_language(final_original_text)

    # 4. normalize_text()
    normalized_text = normalize_text(final_original_text)

    # 5. translate_to_english()
    translated_text = translate_to_english(final_original_text, original_language)

    # 6. content_hash()
    dedup_hash = content_hash(normalized_text)
    # TODO: The caller would typically check this 'dedup_hash' against a store
    # of previously seen hashes to prevent duplicate processing.

    # 7. Assemble and return the output dict
    output_dict = {
        "inquiry_id": str(uuid.uuid4()),
        "channel": channel,
        "original_text": final_original_text,
        "original_language": original_language,
        "normalized_text": normalized_text,
    }

    # Only include 'translated_text' if a translation actually occurred
    # (i.e., source was not English) and the translation is meaningful.
    if original_language != "en" and translated_text and translated_text.strip():
        output_dict["translated_text"] = translated_text
    # If original_language is "en", then 'normalized_text' is already the English canonical form.
    # No separate "translated_text" field is needed as per "optional" and "English canonical" interpretation.

    return output_dict

if __name__ == "__main__":
    print("--- Pipeline Orchestrator Examples ---")

    # Example 1: Text-only inquiry (English)
    try:
        result = process_inquiry(channel="portal", text="This is a test inquiry in English.")
        print("\nResult for English text-only:")
        print(result)
    except ValueError as e:
        print(f"\nError for English text-only: {e}")

    # Example 2: Chat inquiry (list of turns)
    chat_turns = [
        {"speaker": "Customer", "message": "नमस्ते, मुझे एक प्रश्न है।"},
        {"speaker": "Agent", "message": "कृपया अपना प्रश्न बताएं।"}
    ]
    try:
        # Ensure BHASHINI_API_KEY is set for translation to work (even if stubbed)
        # and fastText model is available for language detection.
        result = process_inquiry(channel="chat", text=chat_turns)
        print("\nResult for Hindi chat turns:")
        print(result)
    except ValueError as e:
        print(f"\nError for Hindi chat turns: {e}")

    # Example 3: File-only inquiry (simulated scanned PDF -> OCR/Vision LLM)
    # This requires a dummy image byte and type for demonstration without actual file I/O
    # In a real scenario, you'd load actual image bytes.
    dummy_image_bytes = b"dummy image content" # Replace with actual image bytes for real test
    dummy_image_type = "image/png"
    try:
        # This will likely trigger Vision LLM fallback due to dummy bytes
        result = process_inquiry(channel="email", file_bytes=dummy_image_bytes, file_type=dummy_image_type)
        print("\nResult for simulated image file (OCR/Vision LLM path):")
        print(result)
    except ValueError as e:
        print(f"\nError for simulated image file: {e}")

    # Example 4: No input provided
    try:
        process_inquiry(channel="portal")
    except ValueError as e:
        print(f"\nError for no input (expected): {e}")

    print("\nNote: For full functionality, ensure fastText model is downloaded,")
    print("and ANTHROPIC_API_KEY / BHASHINI_API_KEY are set in your environment.")
