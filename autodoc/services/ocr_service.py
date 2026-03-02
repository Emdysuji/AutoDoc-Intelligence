"""OCR service implementation."""
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path


class OCRService:
    """Extracts textual content from PDF documents."""

    def __init__(self, tesseract_cmd: str | None = None) -> None:
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text(self, file_path: str) -> str:
        pages = convert_from_path(file_path)
        texts: list[str] = []
        for page in pages:
            texts.append(pytesseract.image_to_string(page))
        return "\n".join(texts).strip()
