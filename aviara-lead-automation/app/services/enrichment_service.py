import re

from app.schemas.lead_schema import LeadEnrichmentRequest, LeadEnrichmentResponse


def _company_slug(company: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", company.lower()).strip("-")
    return slug or "unknown-company"


def enrich_lead(lead: LeadEnrichmentRequest) -> LeadEnrichmentResponse:
    company_lower = lead.company.lower()

    if "acme" in company_lower:
        industry = "Technology"
        company_size = "201-500"
    elif "finance" in company_lower or "bank" in company_lower:
        industry = "Finance"
        company_size = "500+"
    elif "health" in company_lower or "care" in company_lower:
        industry = "Healthcare"
        company_size = "101-200"
    else:
        industry = "General Business"
        company_size = "11-50"

    return LeadEnrichmentResponse(
        linkedin_url=f"https://linkedin.com/company/{_company_slug(lead.company)}",
        company_size=company_size,
        industry=industry,
    )
