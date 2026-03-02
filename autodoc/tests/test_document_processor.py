from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from autodoc.app.database import Base
from autodoc.core.document_processor import DocumentProcessor
from autodoc.core.field_extractor import FieldExtractor
from autodoc.models.document import Document


class MockOCR:
    def extract_text(self, _path: str) -> str:
        return "Invoice Number INV-123 Invoice Date 2024-05-01 Total Amount 99.99 Vendor ACME"


class MockClassifier:
    def predict(self, _text: str) -> str:
        return "invoice"


def test_document_processor_success() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    doc = Document(filename="a.pdf", storage_path="/tmp/a.pdf", processing_status="pending")
    db.add(doc)
    db.commit()
    db.refresh(doc)

    processor = DocumentProcessor(MockOCR(), MockClassifier(), FieldExtractor())
    processor.process(db, doc)

    updated = db.get(Document, doc.id)
    assert updated is not None
    assert updated.processing_status == "completed"
    assert updated.document_type == "invoice"
    assert updated.extracted_data["invoice_number"] == "INV-123"
