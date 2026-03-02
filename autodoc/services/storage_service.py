"""Local file storage abstraction."""
import re
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


class StorageService:
    """Handles file persistence in a local filesystem-backed storage."""

    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        safe_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", filename)
        return safe_name or "document.pdf"

    async def store_upload(self, file: UploadFile) -> tuple[str, str]:
        original_name = self.sanitize_filename(file.filename or "document.pdf")
        stored_name = f"{uuid4()}_{original_name}"
        destination = self.base_dir / stored_name

        content = await file.read()
        destination.write_bytes(content)
        await file.seek(0)
        return original_name, str(destination)
