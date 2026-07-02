import os
import sys
from pathlib import Path

# Add the backend directory to the Python path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from ingestion.document_processing.pdf_extractor import extract_pdf_text
from ingestion.document_processing.ocr_engine import run_ocr

# --- Fixture Generation (if files don't exist) ---
FIXTURES_DIR = Path(__file__).resolve().parent.parent / "test_fixtures"
FIXTURES_DIR.mkdir(exist_ok=True)

# Synthetic PDF generation
PDF_FILE = FIXTURES_DIR / "sample_english.pdf"
if not PDF_FILE.exists():
    print(f"Generating synthetic PDF: {PDF_FILE}")
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    import io

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "This is a sample English text for PDF extraction.")
    c.drawString(100, 730, "It contains multiple lines to test the extraction.")
    c.save()
    buffer.seek(0)
    with open(PDF_FILE, "wb") as f:
        f.write(buffer.getvalue())
    print("Synthetic PDF generated.")

# Synthetic PNG generation with Devanagari text
PNG_FILE = FIXTURES_DIR / "sample_hindi.png"
if not PNG_FILE.exists():
    print(f"Generating synthetic PNG: {PNG_FILE}")
    from PIL import Image, ImageDraw, ImageFont
    import textwrap

    try:
        # Try to find a font that supports Devanagari
        # Common fonts: NotoSansDevanagari, Lohit-Devanagari, Arial Unicode MS
        # You might need to adjust this path based on your system
        font_path = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf" # Common Linux path
        if not Path(font_path).exists():
            font_path = "/System/Library/Fonts/Arial Unicode.ttf" # Common macOS path
        if not Path(font_path).exists():
            print("Warning: Devanagari font not found at common paths. Using default PIL font, which may not render Hindi correctly.")
            font = ImageFont.load_default()
        else:
            font = ImageFont.truetype(font_path, 30)
    except Exception as e:
        print(f"Error loading font: {e}. Using default PIL font.")
        font = ImageFont.load_default()

    img_width, img_height = 800, 400
    img = Image.new('RGB', (img_width, img_height), color = (255, 255, 255))
    d = ImageDraw.Draw(img)

    hindi_text = "नमस्ते दुनिया! यह हिंदी में एक नमूना पाठ है।" # "Hello world! This is a sample text in Hindi."
    marathi_text = "नमस्कार जग! हे मराठीमध्ये एक नमुना मजकूर आहे." # "Hello world! This is a sample text in Marathi."

    # Wrap text to fit within image width
    wrapped_hindi = textwrap.fill(hindi_text, width=30)
    wrapped_marathi = textwrap.fill(marathi_text, width=30)

    d.text((50, 50), wrapped_hindi, fill=(0, 0, 0), font=font)
    d.text((50, 150), wrapped_marathi, fill=(0, 0, 0), font=font)

    img.save(PNG_FILE)
    print("Synthetic PNG generated.")

print("\n--- Running Tests ---")

# 1. Load sample PDF and scanned image
print(f"Loading PDF from: {PDF_FILE}")
with open(PDF_FILE, "rb") as f:
    pdf_bytes = f.read()

print(f"Loading PNG from: {PNG_FILE}")
with open(PNG_FILE, "rb") as f:
    image_bytes = f.read()

# 2. Run extract_pdf_text() and run_ocr()
print("\n--- PDF Extraction ---")
extracted_pdf_text = extract_pdf_text(pdf_bytes)
print("Extracted PDF Text:")
print("--------------------")
print(extracted_pdf_text)
print("--------------------")
print(f"PDF text length: {len(extracted_pdf_text.strip())}")
if not extracted_pdf_text.strip():
    print("Note: PDF extraction returned empty, indicating no extractable text layer or error.")

print("\n--- OCR on Image ---")
ocr_text = run_ocr(image_bytes)
print("OCR Extracted Text:")
print("--------------------")
print(ocr_text)
print("--------------------")
print(f"OCR text length: {len(ocr_text.strip())}")
if not ocr_text.strip():
    print("Note: OCR returned empty, indicating no text found or error.")

print("\n--- Test Week 1 Script Finished ---")
