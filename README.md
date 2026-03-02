# AutoDoc Intelligence

AutoDoc Intelligence is a production-style SaaS backend for AI-powered document automation. It ingests business PDFs (invoices, receipts, contracts), extracts text with OCR, classifies document type, parses structured data, and serves results through APIs and an admin dashboard.

## 1) Business Problem Description
Small and medium businesses process high volumes of operational documents manually. This causes delays, data-entry errors, and poor visibility into processing states. AutoDoc Intelligence centralizes document ingestion and automation in a scalable API backend.

## 2) Example Real-World Use Case
An accounting outsourcing company receives 10,000 monthly invoices and receipts from multiple clients. AutoDoc Intelligence lets the company upload documents via API, automatically extract critical fields (vendor, invoice number, totals), and track failures for human review from a dashboard.

## 3) Architecture Diagram (ASCII)
```text
                   +-----------------------+
                   |   Client Apps / UI    |
                   +-----------+-----------+
                               |
                               v
                    +----------------------+
                    | FastAPI Application  |
                    |  - REST APIs         |
                    |  - Jinja Dashboard   |
                    +----------+-----------+
                               |
             +-----------------+-----------------+
             |                                   |
             v                                   v
 +------------------------+            +----------------------+
 | PostgreSQL             |            | Local File Storage   |
 | documents + metadata   |            | original PDFs        |
 +------------------------+            +----------------------+
                               |
                               v
                    +----------------------+
                    | Celery Worker        |
                    | OCR + Classify +     |
                    | Field Extraction     |
                    +----------+-----------+
                               |
                               v
                         +-----------+
                         |  Redis    |
                         |  Broker   |
                         +-----------+
```

## 4) Processing Pipeline Diagram
```text
Upload PDF -> Validate -> Store File -> Create DB Record (pending)
       -> Queue Celery Task -> Status: processing
       -> OCR Extraction -> Document Classification
       -> Type-specific Regex Field Extraction
       -> Save JSON Data + Type -> Status: completed
       -> (on error) Status: failed + error_message
```

## 5) Setup Instructions
### Local Python setup
```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn autodoc.app.main:app --reload
```

### Docker setup (recommended)
```bash
cp .env.example .env
docker compose up --build
```

## 6) API Examples (curl)
### Upload a document
```bash
curl -X POST http://localhost:8000/documents \
  -F "file=@./sample_invoice.pdf"
```

### List all documents
```bash
curl http://localhost:8000/documents
```

### Get one document
```bash
curl http://localhost:8000/documents/1
```

### Get processing status
```bash
curl http://localhost:8000/documents/1/status
```

### Health check
```bash
curl http://localhost:8000/health
```

## 7) Sample Response JSON
```json
{
  "id": 1,
  "filename": "invoice_jan.pdf",
  "upload_timestamp": "2026-03-02T20:30:12.451913",
  "processing_status": "completed",
  "document_type": "invoice",
  "extracted_data": {
    "invoice_number": "INV-1024",
    "invoice_date": "2026-01-15",
    "total_amount": "1899.90",
    "vendor_name": "Acme Supplies Ltd"
  },
  "error_message": null
}
```

## 8) Future Improvements
- Add object storage backends (S3/GCS/Azure Blob) using pluggable storage providers.
- Integrate model registry and model versioning for classifier upgrades.
- Add role-based access control and tenant isolation for multi-tenant SaaS.
- Add OpenTelemetry tracing and metrics (Prometheus/Grafana).
- Add dead letter queue and retry policies for resilient background processing.

## 9) Screenshots
- Dashboard screenshot placeholder: `docs/screenshots/dashboard.png`

## Project Structure
```text
autodoc/
├── app/
├── api/
├── core/
├── models/
├── services/
├── tasks/
├── templates/
└── tests/
```
