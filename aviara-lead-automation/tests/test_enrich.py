from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_successful_enrichment_for_acme_company():
    response = client.post(
        "/api/enrich",
        json={
            "name": "John Doe",
            "email": "john@company.com",
            "company": "Acme Inc",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "linkedin_url": "https://linkedin.com/company/acme-inc",
        "company_size": "201-500",
        "industry": "Technology",
    }


def test_invalid_email_validation():
    response = client.post(
        "/api/enrich",
        json={
            "name": "John Doe",
            "email": "not-an-email",
            "company": "Acme Inc",
        },
    )

    assert response.status_code == 422


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_assignment_enrich_alias():
    response = client.post(
        "/enrich",
        json={
            "name": "Jane Doe",
            "email": "jane@financebank.com",
            "company": "Finance Bank",
        },
    )

    assert response.status_code == 200
    assert response.json()["industry"] == "Finance"
