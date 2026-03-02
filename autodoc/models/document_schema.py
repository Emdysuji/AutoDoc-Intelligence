"""Pydantic schemas for document responses."""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class DocumentBaseResponse(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime
    processing_status: str
    document_type: str | None = None
    extracted_data: dict[str, Any] | None = None
    error_message: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DocumentStatusResponse(BaseModel):
    id: int
    processing_status: str
    error_message: str | None = None


class DocumentListResponse(BaseModel):
    documents: list[DocumentBaseResponse]
