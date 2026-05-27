# Aviara Labs - AI-Powered Lead Automation System

Assignment project for the Aviara Labs AI Automation Engineer role. This project implements an end-to-end lead automation backend with FastAPI and an n8n workflow that receives leads, enriches company data, classifies intent, stores results in Google Sheets, and sends an email notification.

No Docker is used.

## Overview

```text
Lead Webhook
-> n8n validation
-> FastAPI enrichment API
-> FastAPI intent classification API
-> Google Sheets storage
-> Email notification
```

The enrichment and classification logic is deterministic mock logic, as allowed by the assignment. No real LinkedIn API, enrichment API, or LLM API is used.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- pytest
- n8n
- Google Sheets
- Gmail/Email notification

## Features

- `POST /api/enrich` and assignment alias `POST /enrich`
- `POST /api/classify` and assignment alias `POST /classify`
- `GET /health`
- Pydantic input validation
- Clean routers/services/schemas folder structure
- Deterministic mock enrichment
- Deterministic mock intent classification
- Simple logging
- Clean JSON error responses
- pytest test coverage
- n8n workflow export
- Architecture and Loom walkthrough docs

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

## Setup

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the FastAPI server:

```powershell
uvicorn app.main:app --reload
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## Run Tests

```powershell
python -m pytest -q
```

Expected result:

```text
7 passed
```

## API Examples

### Enrichment

Endpoint:

```text
POST /api/enrich
POST /enrich
```

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

PowerShell test:

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

### Intent Classification

Endpoint:

```text
POST /api/classify
POST /classify
```

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

PowerShell test:

```powershell
$body = @{
  message = "I am interested in your services"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/classify" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

## Mock Logic

Enrichment:

- Company contains `acme`: Technology, `201-500`
- Company contains `finance` or `bank`: Finance, `500+`
- Company contains `health` or `care`: Healthcare, `101-200`
- Otherwise: General Business, `11-50`
- LinkedIn URL is generated from a company-name slug

Classification:

- Sales enquiry: `interested`, `pricing`, `demo`, `buy`, `services`, `sales`
- Support request: `issue`, `problem`, `not working`, `help`, `error`, `support`
- Partnership: `partner`, `collaboration`, `integrate`, `business together`
- Unknown: ambiguous/noisy input with confidence `0.55`

## n8n Workflow

Workflow export:

```text
workflows/n8n_workflow_export_sample.json
```

Workflow nodes:

- Webhook Trigger
- Validate Input
- HTTP Request: Call Enrichment API
- HTTP Request: Call Classification API
- Prepare Storage Record
- Google Sheets storage
- Email notification
- Error Handling Path

Start n8n locally:

```powershell
npx n8n
```

Open:

```text
http://localhost:5678
```

Import the workflow JSON into n8n, then click **Execute Workflow**.

Test webhook payload:

```powershell
$body = @{
  name = "John Doe"
  email = "john@company.com"
  company = "Acme Inc"
  message = "I am interested in your services"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5678/webhook-test/aviara-lead-webhook" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

## Google Sheets Setup

Create a Google Sheet with these headers in row 1:

```text
email
name
company
message
linkedin_url
company_size
industry
intent
confidence
processed_at
idempotency_key
```

In n8n, configure the Google Sheets node:

```text
Resource: Sheet Within Document
Operation: Append Row
Document: your spreadsheet
Sheet: Sheet1
Mapping Column Mode: Map Each Column Manually
```

Map columns from the `Prepare Storage Record` node:

```text
email              {{$json.email}}
name               {{$json.name}}
company            {{$json.company}}
message            {{$json.message}}
linkedin_url       {{$json.linkedin_url}}
company_size       {{$json.company_size}}
industry           {{$json.industry}}
intent             {{$json.intent}}
confidence         {{$json.confidence}}
processed_at       {{$json.processed_at}}
idempotency_key    {{$json.idempotency_key}}
```

Use Expression mode in n8n for each mapping.

## Email Setup

Use either the Gmail node or Email Send node.

Recommended Gmail node:

```text
Resource: Message
Operation: Send
To: your email
Subject: New lead processed: {{$node["Prepare Storage Record"].json.name}}
```

Email body:

```text
New lead processed successfully.

Name: {{$node["Prepare Storage Record"].json.name}}
Email: {{$node["Prepare Storage Record"].json.email}}
Company: {{$node["Prepare Storage Record"].json.company}}
Industry: {{$node["Prepare Storage Record"].json.industry}}
Company Size: {{$node["Prepare Storage Record"].json.company_size}}
Intent: {{$node["Prepare Storage Record"].json.intent}}
Confidence: {{$node["Prepare Storage Record"].json.confidence}}
LinkedIn: {{$node["Prepare Storage Record"].json.linkedin_url}}
```

For Google OAuth, enable these APIs in Google Cloud:

- Google Sheets API
- Google Drive API
- Gmail API

Do not commit OAuth client secret JSON files.

## Error Handling

- Pydantic returns `422` for invalid API payloads.
- Routers catch unexpected failures and return clean `500` responses.
- n8n validates required fields before API calls.
- Error branch captures invalid webhook payloads.
- Application logs enrichment, classification, and error events.

## Idempotency

Email is treated as the unique lead key. In production, Google Sheets/Airtable should upsert by email instead of blindly appending duplicate rows.

## Scalability

For 1000+ leads/hour:

- Keep n8n as the orchestrator only.
- Move heavy processing into backend workers.
- Add Redis or RabbitMQ as a queue.
- Use Celery workers for enrichment, classification, storage, and notification.
- Scale FastAPI horizontally behind a load balancer.
- Scale workers independently based on queue depth.
- Batch storage writes where possible.

## Reliability

- Add retry policies to n8n HTTP, storage, and notification nodes.
- Use fallback enrichment values for unknown company data.
- Add rate limiting on backend APIs.
- Use a dead-letter queue for repeatedly failed jobs.
- Store execution logs and processing status for auditability.

## Loom Walkthrough

Recommended walkthrough:

1. Show project structure.
2. Start FastAPI and open `/docs`.
3. Demonstrate `/health`, `/api/enrich`, and `/api/classify`.
4. Show n8n workflow design.
5. Send a webhook test request.
6. Show Google Sheet row creation.
7. Show email notification received.
8. Explain idempotency, scalability, and reliability.

See:

```text
docs/loom_walkthrough.md
docs/architecture.md
docs/submission_checklist.md
```

## Security Notes

- Do not commit `.env`.
- Do not commit Google OAuth client secret JSON files.
- If a client secret is exposed, rotate/delete it in Google Cloud and create a new one.
