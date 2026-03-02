"""Regex-based field extraction for supported document types."""
import re
from collections.abc import Callable

ExtractorFn = Callable[[str], dict[str, object]]


class FieldExtractor:
    """Extracts structured fields based on document type-specific patterns."""

    def __init__(self) -> None:
        self._extractors: dict[str, ExtractorFn] = {
            "invoice": self._extract_invoice,
            "receipt": self._extract_receipt,
            "contract": self._extract_contract,
        }

    def extract(self, document_type: str, text: str) -> dict[str, object]:
        extractor = self._extractors.get(document_type)
        if not extractor:
            return {}
        return extractor(text)

    def _extract_invoice(self, text: str) -> dict[str, object]:
        return {
            "invoice_number": self._search(r"invoice\s*(?:number|#)?\s*[:\-]?\s*([A-Z0-9-]+)", text),
            "invoice_date": self._search(r"(?:invoice\s*date|date)\s*[:\-]?\s*(\d{4}-\d{2}-\d{2})", text),
            "total_amount": self._search(r"(?:total\s*(?:amount)?|amount\s*due)\s*[:\-]?\s*\$?([0-9]+(?:\.[0-9]{2})?)", text),
            "vendor_name": self._search(r"(?:vendor|from)\s*[:\-]?\s*([A-Za-z0-9 .,&'-]+)", text),
        }

    def _extract_receipt(self, text: str) -> dict[str, object]:
        return {
            "merchant_name": self._search(r"(?:merchant|receipt\s*from|from)\s*[:\-]?\s*([A-Za-z0-9 .,&'-]+)", text),
            "date": self._search(r"date\s*[:\-]?\s*(\d{4}-\d{2}-\d{2})", text),
            "total_amount": self._search(r"(?:total\s*(?:paid)?|amount)\s*[:\-]?\s*\$?([0-9]+(?:\.[0-9]{2})?)", text),
        }

    def _extract_contract(self, text: str) -> dict[str, object]:
        party_a = self._search(r"between\s+([A-Za-z0-9 .,&'-]+?)\s+and", text)
        party_b = self._search(r"and\s+([A-Za-z0-9 .,&'-]+?)\s+(?:effective|dated|on)", text)
        return {
            "party_names": [p for p in [party_a, party_b] if p],
            "contract_date": self._search(r"(?:effective\s*date|contract\s*date|dated)\s*[:\-]?\s*(\d{4}-\d{2}-\d{2})", text),
        }

    @staticmethod
    def _search(pattern: str, text: str) -> str | None:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        return match.group(1).strip() if match else None
