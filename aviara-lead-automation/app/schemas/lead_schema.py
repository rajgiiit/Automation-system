from pydantic import BaseModel, EmailStr, Field


class LeadEnrichmentRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    company: str = Field(..., min_length=2)


class LeadEnrichmentResponse(BaseModel):
    linkedin_url: str
    company_size: str
    industry: str
