import pytest
import os
import sys
from pathlib import Path
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Add the project root directory to the Python path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Define fixture directory
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
FIXTURES_DIR.mkdir(exist_ok=True)

@pytest.fixture(scope="session")
def synthetic_pdf_with_text():
    """Generates a synthetic PDF with extractable English text."""
    pdf_path = FIXTURES_DIR / "synthetic_text.pdf"
    if not pdf_path.exists():
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "This is a sample English text for PDF extraction.")
        c.drawString(100, 730, "It contains multiple lines to test the extraction.")
        c.save()
        buffer.seek(0)
        with open(pdf_path, "wb") as f:
            f.write(buffer.getvalue())
    with open(pdf_path, "rb") as f:
        yield f.read()
    # No cleanup, keep fixtures for inspection

@pytest.fixture(scope="session")
def synthetic_scanned_pdf():
    """Generates a synthetic PDF that appears scanned (no text layer)."""
    # This is a bit tricky with reportlab. A simple way to simulate "scanned"
    # is to draw text as shapes or an image, but for simplicity, we'll create
    # a PDF with minimal text that extract_pdf_text might miss, or an image.
    # For a true scanned PDF, one would typically embed an image.
    # For now, we'll create a PDF with very little text, or just an image.
    # A more robust solution would involve rasterizing an image into a PDF.
    # For the purpose of this test, we'll create a PDF that *should* return ""
    # from extract_pdf_text, perhaps by drawing very small text or just an image.
    # Let's create a PDF with an embedded image to simulate a scanned document.
    pdf_path = FIXTURES_DIR / "synthetic_scanned.pdf"
    if not pdf_path.exists():
        # Create a dummy image first
        img_width, img_height = 200, 100
        img = Image.new('RGB', (img_width, img_height), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        d.text((10, 10), "Scanned Image", fill=(0, 0, 0), font=ImageFont.load_default())
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        # Embed the image
        c.drawImage(Image.open(img_buffer), 100, 600, width=img_width, height=img_height)
        c.save()
        buffer.seek(0)
        with open(pdf_path, "wb") as f:
            f.write(buffer.getvalue())
    with open(pdf_path, "rb") as f:
        yield f.read()

@pytest.fixture(scope="session")
def synthetic_image_en():
    """Generates a synthetic PNG with English text."""
    img_path = FIXTURES_DIR / "synthetic_en.png"
    if not img_path.exists():
        img_width, img_height = 400, 200
        img = Image.new('RGB', (img_width, img_height), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        d.text((50, 50), "Hello World! This is English text.", fill=(0, 0, 0), font=font)
        img.save(img_path)
    with open(img_path, "rb") as f:
        yield f.read()

@pytest.fixture(scope="session")
def synthetic_image_hi():
    """Generates a synthetic PNG with Hindi (Devanagari) text."""
    img_path = FIXTURES_DIR / "synthetic_hi.png"
    if not img_path.exists():
        img_width, img_height = 600, 300
        img = Image.new('RGB', (img_width, img_height), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        try:
            font_path = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf"
            if not Path(font_path).exists():
                font_path = "/System/Library/Fonts/Arial Unicode.ttf"
            if not Path(font_path).exists():
                font = ImageFont.load_default()
                print("Warning: Devanagari font not found for synthetic_image_hi. Using default font.")
            else:
                font = ImageFont.truetype(font_path, 30)
        except Exception:
            font = ImageFont.load_default()
            print("Warning: Error loading Devanagari font for synthetic_image_hi. Using default font.")

        hindi_text = "नमस्ते दुनिया! यह हिंदी में एक नमूना पाठ है।"
        wrapped_hindi = textwrap.fill(hindi_text, width=30)
        d.text((50, 50), wrapped_hindi, fill=(0, 0, 0), font=font)
        img.save(img_path)
    with open(img_path, "rb") as f:
        yield f.read()

@pytest.fixture(scope="session")
def synthetic_image_mr():
    """Generates a synthetic PNG with Marathi (Devanagari) text."""
    img_path = FIXTURES_DIR / "synthetic_mr.png"
    if not img_path.exists():
        img_width, img_height = 600, 300
        img = Image.new('RGB', (img_width, img_height), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        try:
            font_path = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf"
            if not Path(font_path).exists():
                font_path = "/System/Library/Fonts/Arial Unicode.ttf"
            if not Path(font_path).exists():
                font = ImageFont.load_default()
                print("Warning: Devanagari font not found for synthetic_image_mr. Using default font.")
            else:
                font = ImageFont.truetype(font_path, 30)
        except Exception:
            font = ImageFont.load_default()
            print("Warning: Error loading Devanagari font for synthetic_image_mr. Using default font.")

        marathi_text = "नमस्कार जग! हे मराठीमध्ये एक नमुना मजकूर आहे."
        wrapped_marathi = textwrap.fill(marathi_text, width=30)
        d.text((50, 50), wrapped_marathi, fill=(0, 0, 0), font=font)
        img.save(img_path)
    with open(img_path, "rb") as f:
        yield f.read()
