from autodoc.core.field_extractor import FieldExtractor


def test_extract_invoice_fields() -> None:
    extractor = FieldExtractor()
    text = "Invoice Number: INV-200 Invoice Date: 2024-01-21 Total Amount: 345.99 Vendor: ACME Ltd"
    fields = extractor.extract("invoice", text)
    assert fields["invoice_number"] == "INV-200"
    assert fields["invoice_date"] == "2024-01-21"
    assert fields["total_amount"] == "345.99"
    assert fields["vendor_name"] == "ACME Ltd"
