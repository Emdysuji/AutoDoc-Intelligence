"""Document management API endpoints."""
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from autodoc.app.config import get_settings
from autodoc.app.database import get_db
from autodoc.models.document import Document
from autodoc.models.document_schema import DocumentBaseResponse, DocumentListResponse, DocumentStatusResponse
from autodoc.services.logging_service import get_logger
from autodoc.services.storage_service import StorageService
from autodoc.tasks.processing_tasks import process_document_task

router = APIRouter(tags=["documents"])
settings = get_settings()
logger = get_logger(__name__)
storage_service = StorageService(settings.local_storage_path)
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))


@router.post("/documents", response_model=DocumentBaseResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)) -> Document:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()
    if len(file_bytes) > settings.max_file_size_bytes:
        raise HTTPException(status_code=400, detail="File too large")
    await file.seek(0)

    filename, storage_path = await storage_service.store_upload(file)

    document = Document(filename=filename, storage_path=storage_path, processing_status="pending")
    db.add(document)
    db.commit()
    db.refresh(document)

    logger.info("document_uploaded", extra={"document_id": document.id})
    process_document_task.delay(document.id)
    return document


@router.get("/documents", response_model=DocumentListResponse)
def list_documents(db: Session = Depends(get_db)) -> DocumentListResponse:
    documents = db.query(Document).order_by(Document.upload_timestamp.desc()).all()
    return DocumentListResponse(documents=documents)


@router.get("/documents/{document_id}", response_model=DocumentBaseResponse)
def get_document(document_id: int, db: Session = Depends(get_db)) -> Document:
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("/documents/{document_id}/status", response_model=DocumentStatusResponse)
def get_status(document_id: int, db: Session = Depends(get_db)) -> DocumentStatusResponse:
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentStatusResponse(id=document.id, processing_status=document.processing_status, error_message=document.error_message)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    documents = db.query(Document).order_by(Document.upload_timestamp.desc()).all()
    failed_jobs = [doc for doc in documents if doc.processing_status == "failed"]
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {"documents": documents, "failed_jobs": failed_jobs},
    )
