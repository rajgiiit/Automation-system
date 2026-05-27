from pydantic import BaseModel, Field


class ClassificationRequest(BaseModel):
    message: str = Field(..., min_length=3)


class ClassificationResponse(BaseModel):
    intent: str
    confidence: float
