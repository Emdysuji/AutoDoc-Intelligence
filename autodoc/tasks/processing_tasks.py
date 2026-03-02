"""Celery task definitions for async processing."""
from celery import Celery

from autodoc.app.config import get_settings
from autodoc.app.database import SessionLocal
from autodoc.core.classifier import SklearnDocumentClassifier
from autodoc.core.document_processor import DocumentProcessor
from autodoc.core.field_extractor import FieldExtractor
from autodoc.models.document import Document
from autodoc.services.ocr_service import OCRService

settings = get_settings()
celery_app = Celery(
    "autodoc_tasks",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)


@celery_app.task(name="autodoc.process_document")
def process_document_task(document_id: int) -> None:
    db = SessionLocal()
    try:
        document = db.get(Document, document_id)
        if not document:
            return
        processor = DocumentProcessor(
            ocr_service=OCRService(settings.tesseract_cmd),
            classifier=SklearnDocumentClassifier(),
            field_extractor=FieldExtractor(),
        )
        processor.process(db, document)
    finally:
        db.close()
