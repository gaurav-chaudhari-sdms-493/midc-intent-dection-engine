import fitz # PyMuPDF

def extract_pdf_text(file_bytes: bytes) -> str:
    """
    Extracts text from PDF file bytes using PyMuPDF.

    Args:
        file_bytes: The content of the PDF file as bytes.

    Returns:
        A string containing the extracted text. Returns an empty string
        if the PDF has no extractable text layer (e.g., it's a scanned
        document without embedded text). An empty string indicates that
        the document likely needs OCR processing.
    """
    document_text = ""
    try:
        document = fitz.open(stream=file_bytes, filetype="pdf")
        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            document_text += page.get_text()
        document.close()
    except Exception as e:
        # Log the exception if necessary, but for this contract,
        # an empty string is the expected output for unextractable text.
        print(f"Error extracting text from PDF: {e}")
        return "" # Return empty string on error or if no text is found

    # If the extracted text is only whitespace or very short,
    # it might indicate no meaningful text layer.
    if not document_text.strip():
        return ""

    return document_text

if __name__ == "__main__":
    # Example Usage:
    # To test, replace 'path/to/your/document.pdf' with an actual PDF file.
    # For a PDF with extractable text:
    # with open("path/to/your/document.pdf", "rb") as f:
    #     pdf_content = f.read()
    #     extracted_text = extract_pdf_text(pdf_content)
    #     print("Extracted Text (with text layer):")
    #     print(extracted_text[:500]) # Print first 500 chars

    # For a scanned PDF without an extractable text layer (expected to return ""):
    # with open("path/to/your/scanned_document.pdf", "rb") as f:
    #     scanned_pdf_content = f.read()
    #     scanned_extracted_text = extract_pdf_text(scanned_pdf_content)
    #     print("\nExtracted Text (scanned, no text layer):")
    #     print(f"'{scanned_extracted_text}' (Expected: '')")
    pass
