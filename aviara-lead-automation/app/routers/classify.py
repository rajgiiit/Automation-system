from fastapi import APIRouter, HTTPException, status

from app.schemas.classify_schema import ClassificationRequest, ClassificationResponse
from app.services.classification_service import classify_message
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/classify",
    response_model=ClassificationResponse,
    status_code=status.HTTP_200_OK,
)
def classify_message_endpoint(payload: ClassificationRequest) -> ClassificationResponse:
    try:
        result = classify_message(payload.message)
        logger.info(
            "Classification completed intent=%s confidence=%s",
            result.intent,
            result.confidence,
        )
        return result
    except Exception as exc:
        logger.exception("Failed to classify message")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to classify message at this time.",
        ) from exc
