from PIL import Image

from autodoc.services.ocr_service import OCRService


class DummyOCR(OCRService):
    def __init__(self) -> None:
        pass


def test_ocr_service_extract_text(monkeypatch) -> None:
    monkeypatch.setattr("autodoc.services.ocr_service.convert_from_path", lambda _path: [Image.new("RGB", (10, 10))])
    monkeypatch.setattr("autodoc.services.ocr_service.pytesseract.image_to_string", lambda _img: "hello world")

    service = DummyOCR()
    assert service.extract_text("sample.pdf") == "hello world"
