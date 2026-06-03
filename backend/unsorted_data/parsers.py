"""Parsers for PDFs, images, text, and logs."""
import os
import mimetypes
try:
    import magic
except Exception:
    magic = None

# PDF text extraction
try:
    from pdfminer.high_level import extract_text as pdf_extract_text
except Exception:
    pdf_extract_text = None

# Pillow for images
try:
    from PIL import Image
except Exception:
    Image = None

# pytesseract optional
try:
    import pytesseract
except Exception:
    pytesseract = None


def detect_mime(path):
    if magic:
        try:
            m = magic.from_file(path, mime=True)
            return m
        except Exception:
            pass
    mt, _ = mimetypes.guess_type(path)
    return mt or "application/octet-stream"


def extract_text(path, ocr=False):
    mt = detect_mime(path) or ""
    if mt.startswith("text"):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            return None
    if mt in ("application/pdf", "application/x-pdf") and pdf_extract_text:
        try:
            return pdf_extract_text(path)
        except Exception:
            return None
    if mt.startswith("image") and Image:
        if ocr and pytesseract:
            try:
                img = Image.open(path)
                return pytesseract.image_to_string(img)
            except Exception:
                return None
    return None


def generate_thumbnail(path, max_dim=400):
    if not Image:
        return None
    try:
        with Image.open(path) as im:
            im.thumbnail((max_dim, max_dim))
            from io import BytesIO
            buf = BytesIO()
            im.save(buf, format="PNG")
            return buf.getvalue()
    except Exception:
        return None
