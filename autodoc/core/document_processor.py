"""Document processing orchestration."""
from sqlalchemy.orm import Session

from autodoc.core.classifier import BaseDocumentClassifier
from autodoc.core.field_extractor import FieldExtractor
from autodoc.models.document import Document
from autodoc.services.logging_service import get_logger
from autodoc.services.ocr_service import OCRService

logger = get_logger(__name__)


class DocumentProcessor:
    """Coordinates OCR, classification, extraction, and persistence."""

    def __init__(
        self,
        ocr_service: OCRService,
        classifier: BaseDocumentClassifier,
        field_extractor: FieldExtractor,
    ) -> None:
        self.ocr_service = ocr_service
        self.classifier = classifier
        self.field_extractor = field_extractor

    def process(self, db: Session, document: Document) -> None:
        try:
            document.processing_status = "processing"
            db.commit()
            db.refresh(document)

            text = self.ocr_service.extract_text(document.storage_path)
            doc_type = self.classifier.predict(text)
            extracted = self.field_extractor.extract(doc_type, text)

            document.processing_status = "completed"
            document.document_type = doc_type
            document.extracted_data = extracted
            document.error_message = None
            db.commit()
            logger.info("document_processing_completed", extra={"document_id": document.id})
        except Exception as exc:
            db.rollback()
            document.processing_status = "failed"
            document.error_message = str(exc)
            db.add(document)
            db.commit()
            logger.exception("document_processing_failed", extra={"document_id": document.id})
