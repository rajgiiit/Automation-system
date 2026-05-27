from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_sales_intent_classification():
    response = client.post(
        "/api/classify",
        json={"message": "I am interested in your services"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "intent": "sales_enquiry",
        "confidence": 0.92,
    }


def test_unknown_intent_classification():
    response = client.post(
        "/api/classify",
        json={"message": "Just saying hello today"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "intent": "unknown",
        "confidence": 0.55,
    }


def test_assignment_classify_alias():
    response = client.post(
        "/classify",
        json={"message": "Can we explore a partner collaboration?"},
    )

    assert response.status_code == 200
    assert response.json()["intent"] == "partnership"
