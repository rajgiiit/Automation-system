from app.schemas.classify_schema import ClassificationResponse

SALES_KEYWORDS = ("interested", "pricing", "demo", "buy", "services", "sales")
SUPPORT_KEYWORDS = ("issue", "problem", "not working", "help", "error", "support")
PARTNERSHIP_KEYWORDS = ("partner", "collaboration", "integrate", "business together")


def _contains_keyword(message: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in message for keyword in keywords)


def classify_message(message: str) -> ClassificationResponse:
    normalized_message = message.lower().strip()

    if _contains_keyword(normalized_message, SALES_KEYWORDS):
        return ClassificationResponse(intent="sales_enquiry", confidence=0.92)

    if _contains_keyword(normalized_message, SUPPORT_KEYWORDS):
        return ClassificationResponse(intent="support_request", confidence=0.9)

    if _contains_keyword(normalized_message, PARTNERSHIP_KEYWORDS):
        return ClassificationResponse(intent="partnership", confidence=0.88)

    return ClassificationResponse(intent="unknown", confidence=0.55)
