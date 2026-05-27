from fastapi import APIRouter, HTTPException, status

from app.schemas.lead_schema import LeadEnrichmentRequest, LeadEnrichmentResponse
from app.services.enrichment_service import enrich_lead
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/enrich",
    response_model=LeadEnrichmentResponse,
    status_code=status.HTTP_200_OK,
)
def enrich_lead_endpoint(payload: LeadEnrichmentRequest) -> LeadEnrichmentResponse:
    try:
        logger.info("Processing enrichment request for company=%s", payload.company)
        return enrich_lead(payload)
    except Exception as exc:
        logger.exception("Failed to enrich lead")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to enrich lead at this time.",
        ) from exc
