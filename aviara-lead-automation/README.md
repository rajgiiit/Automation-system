# Aviara Labs - AI-Powered Lead Automation System

Backend service for the Aviara Labs AI Automation Engineer assignment. The project provides simple FastAPI endpoints that can be called from an n8n workflow to enrich incoming leads, classify lead intent, store results, and trigger notifications.

## Assignment Overview

Expected automation flow:

```text
Webhook/n8n receives lead
-> validates input
-> calls FastAPI /api/enrich
-> calls FastAPI /api/classify
-> stores result in Google Sheets or Airtable
-> sends notification
```

This implementation uses deterministic mock logic only. It does not call LinkedIn, real enrichment APIs, or LLM APIs.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- pytest
- n8n-compatible HTTP workflow design

## Folder Structure

```text
aviara-lead-automation/
|-- app/
|   |-- main.py
|   |-- routers/
|   |   |-- enrich.py
|   |   `-- classify.py
|   |-- services/
|   |   |-- enrichment_service.py
|   |   `-- classification_service.py
|   |-- schemas/
|   |   |-- lead_schema.py
|   |   `-- classify_schema.py
|   `-- utils/
|       `-- logger.py
|-- workflows/
|   `-- n8n_workflow_export_sample.json
|-- docs/
|   |-- architecture.md
|   |-- loom_walkthrough.md
|   `-- submission_checklist.md
|-- tests/
|   |-- test_enrich.py
|   `-- test_classify.py
|-- requirements.txt
|-- .env.example
|-- README.md
`-- .gitignore
```

## Setup Without Docker

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Optionally create a local environment file:

```bash
cp .env.example .env
```

Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

Run tests:

```bash
python -m pytest -q
```

## API Examples

### POST /api/enrich

The assignment-compatible alias `POST /enrich` is also available.

Request:

```json
{
  "name": "John Doe",
  "email": "john@company.com",
  "company": "Acme Inc"
}
```

Response:

```json
{
  "linkedin_url": "https://linkedin.com/company/acme-inc",
  "company_size": "201-500",
  "industry": "Technology"
}
```

cURL:

```bash
curl -X POST "http://127.0.0.1:8000/api/enrich" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"John Doe\",\"email\":\"john@company.com\",\"company\":\"Acme Inc\"}"
```

PowerShell:

```powershell
$body = @{
  name = "John Doe"
  email = "john@company.com"
  company = "Acme Inc"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/enrich" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

### POST /api/classify

The assignment-compatible alias `POST /classify` is also available.

Request:

```json
{
  "message": "I am interested in your services"
}
```

Response:

```json
{
  "intent": "sales_enquiry",
  "confidence": 0.92
}
```

cURL:

```bash
curl -X POST "http://127.0.0.1:8000/api/classify" \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"I am interested in your services\"}"
```

PowerShell:

```powershell
$body = @{
  message = "I am interested in your services"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/classify" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

## n8n Workflow Explanation

The n8n workflow export is available at `workflows/n8n_workflow_export_sample.json`. It is designed to be imported into n8n as an assignment-ready workflow structure. It contains these nodes:

- Webhook Trigger
- Validate Input
- HTTP Request: Call Enrichment API
- HTTP Request: Call Classification API
- Prepare Storage Record
- Google Sheets/Airtable Storage
- Slack/Email Notification
- Error Handling Path

The storage and notification nodes are placeholder Set nodes so the workflow can be reviewed without requiring private Google, Airtable, Slack, or email credentials. In a real n8n account, replace those placeholders with real Google Sheets/Airtable and Slack/Email nodes.

## End-to-End n8n Demo

1. Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

2. Import `workflows/n8n_workflow_export_sample.json` into n8n.

3. In n8n, open the workflow and select **Execute Workflow**.

4. Send this JSON payload to the n8n webhook URL:

```json
{
  "name": "John Doe",
  "email": "john@company.com",
  "company": "Acme Inc",
  "message": "I am interested in your services"
}
```

5. Confirm the final output includes:

- Original lead fields
- `linkedin_url`
- `company_size`
- `industry`
- `intent`
- `confidence`
- notification text

## Connecting n8n With Local FastAPI

If n8n is running locally, use:

```text
http://127.0.0.1:8000/api/enrich
http://127.0.0.1:8000/api/classify
```

If using n8n Cloud, expose your local FastAPI server with a tunneling tool such as ngrok:

```bash
ngrok http 8000
```

Then use the generated HTTPS URL in the n8n HTTP Request nodes.

## Storage and Notification Integration

For a real submission demo, replace the placeholder `Google Sheets/Airtable Storage` node with either:

- Google Sheets lookup by email, then update or append row
- Airtable upsert using email as the unique key

Replace the placeholder `Slack/Email Notification` node with either:

- Slack message node
- Email node
- Webhook notification node

The workflow is intentionally structured so these replacements do not change the backend API or business logic.

## Error Handling Strategy

Pydantic validates incoming request data and returns `422` for invalid payloads. Route handlers catch unexpected exceptions, log them, and return clean `500` JSON errors without exposing internal stack traces.

## Idempotency Strategy

Use email as the unique lead key. In Google Sheets or Airtable, search by email before inserting. If the email already exists, update the existing row with the latest enrichment, classification, and timestamp.

## Scalability for 1000+ Leads/Hour

n8n should orchestrate the process and avoid doing heavy processing itself. For higher volume, add Redis or RabbitMQ as a queue, process jobs with Celery workers, and scale FastAPI plus workers horizontally. Batch writes to Google Sheets/Airtable where possible and enforce rate limits for external systems.

## Reliability

Use n8n retry settings for temporary failures, fallback values for unknown enrichment fields, and a dead-letter queue for repeatedly failed jobs. Keep backend logs, n8n execution logs, and storage status fields so every lead can be audited.

## Loom Walkthrough Points

- Show FastAPI project structure and separation of routers, schemas, and services.
- Demonstrate `/docs`, `/health`, `/api/enrich`, `/enrich`, `/api/classify`, and `/classify`.
- Explain deterministic mock enrichment and classification logic.
- Walk through the n8n workflow node structure.
- Explain idempotency with email as the unique key.
- Discuss scaling with queues, workers, and horizontal FastAPI instances.
- Discuss reliability with retries, fallback values, logs, and dead-letter handling.

See `docs/loom_walkthrough.md` for a recording script and `docs/submission_checklist.md` for final submission tracking.
