# Loom Walkthrough Guide

Use this as a 5-10 minute recording script.

## 1. Project Overview

- Show the repository root.
- Mention this is a Python + FastAPI backend with an n8n workflow export.
- Mention no Docker, no real LinkedIn API, and no real LLM API are used.

## 2. FastAPI Code Structure

- `app/main.py`: app setup, health route, router registration.
- `app/routers`: HTTP endpoints.
- `app/services`: deterministic enrichment and classification logic.
- `app/schemas`: Pydantic validation.
- `app/utils/logger.py`: simple logging setup.

## 3. Backend Demo

Start the server:

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Show:

- `GET /health`
- `POST /api/enrich`
- `POST /api/classify`
- Assignment-compatible aliases: `POST /enrich` and `POST /classify`

## 4. n8n Workflow Demo

- Import `workflows/n8n_workflow_export_sample.json` into n8n.
- Show nodes:
  - Webhook Trigger
  - Validate Input
  - HTTP Request: Call Enrichment API
  - HTTP Request: Call Classification API
  - Prepare Storage Record
  - Google Sheets/Airtable Storage
  - Slack/Email Notification
  - Error Handling Path
- Explain that storage and notification are placeholder Set nodes in the export and should be replaced with real Google Sheets/Airtable and Slack/Email credentials in a live account.

## 5. End-to-End Demo

Send this payload to the n8n webhook:

```json
{
  "name": "John Doe",
  "email": "john@company.com",
  "company": "Acme Inc",
  "message": "I am interested in your services"
}
```

Show the final workflow output containing:

- Enriched company data
- Intent classification
- Storage payload
- Notification text

## 6. System Design Decisions

- n8n orchestrates the workflow.
- FastAPI owns business logic.
- Email is used as the idempotency key.
- For 1000+ leads/hour, add Redis/RabbitMQ, Celery workers, horizontal FastAPI scaling, retries, and a dead-letter queue.

## 7. Reliability

- Pydantic handles invalid API input.
- n8n validates required fields before API calls.
- Backend logs processing events and errors.
- Production workflow should add retries, rate limits, failure alerts, and dead-letter handling.
