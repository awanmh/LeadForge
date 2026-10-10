from unittest.mock import MagicMock
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.db.session import SessionLocal, get_db
from app.main import app
from app.core.security import rate_limiter


def test_post_valid_lead(client):
    payload = {
        "name": "Alex Mercer",
        "email": "alex@forma-client.example",
        "service_slug": "web-development",
        "message": "We need an editorial, search-optimized website.",
        "website": "",
    }
    response = client.post("/api/v1/leads", json=payload)
    assert response.status_code == 201
    assert response.json() == {"message": "Inquiry received."}

    # Verify exactly one record inserted in database (T-03)
    db = SessionLocal()
    try:
        leads = db.execute(text("SELECT id, name, email, service_slug, message, status FROM leads")).fetchall()
        assert len(leads) == 1
        assert leads[0].name == "Alex Mercer"
        assert leads[0].email == "alex@forma-client.example"
        assert leads[0].service_slug == "web-development"
        assert leads[0].status == "new"
    finally:
        db.close()


def test_post_honeypot_does_not_persist(client):
    # Non-empty honeypot yields generic response; zero inserts (T-02)
    payload = {
        "name": "Bot Spammer",
        "email": "bot@spam.example",
        "message": "Buy cheap watches now immediately!",
        "website": "http://spam-link.example",
    }
    response = client.post("/api/v1/leads", json=payload)
    assert response.status_code == 201
    assert response.json() == {"message": "Inquiry received."}

    db = SessionLocal()
    try:
        count = db.execute(text("SELECT COUNT(*) FROM leads")).scalar()
        assert count == 0
    finally:
        db.close()


def test_post_invalid_schema_returns_422(client):
    payload = {
        "name": "A",  # too short (< 2)
        "email": "invalid-email-address",
        "message": "short",  # too short (< 10)
    }
    response = client.post("/api/v1/leads", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "errors" in data
    assert any(err["field"] == "name" for err in data["errors"])
    assert any(err["field"] == "email" for err in data["errors"])


def test_rate_limiting_enforcement(client):
    # Reset limiter for clean test
    rate_limiter.requests.clear()
    payload = {
        "name": "Rate Limited User",
        "email": "test@rate.example",
        "message": "Testing rate limit threshold triggers.",
        "website": "",
    }

    # 10 requests allowed
    for _ in range(10):
        res = client.post("/api/v1/leads", json=payload)
        assert res.status_code == 201

    # 11th request must return 429 (T-05)
    res_overflow = client.post("/api/v1/leads", json=payload)
    assert res_overflow.status_code == 429
    assert "Too many requests" in res_overflow.json()["detail"]


def test_database_outage_returns_503(client):
    mock_db = MagicMock()
    mock_db.commit.side_effect = OperationalError("connection refused", None, None)

    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        payload = {
            "name": "Valid User",
            "email": "valid@example.com",
            "message": "Testing DB failure handling.",
            "website": "",
        }
        res = client.post("/api/v1/leads", json=payload)
        assert res.status_code == 503
        # Ensure no sensitive stack trace or SQL leakage
        assert "temporarily unavailable" in res.json()["detail"].lower()
    finally:
        app.dependency_overrides.clear()
