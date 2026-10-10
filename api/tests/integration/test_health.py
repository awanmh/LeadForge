from unittest.mock import MagicMock
from sqlalchemy.exc import OperationalError
from app.main import app
from app.db.session import get_db


def test_liveness_endpoint(client):
    res = client.get("/health/live")
    assert res.status_code == 200
    assert res.json() == {"status": "live"}


def test_readiness_endpoint_healthy(client):
    res = client.get("/health/ready")
    assert res.status_code == 200
    assert res.json() == {"status": "ready", "database": "connected"}


def test_readiness_endpoint_unhealthy_when_db_down(client):
    mock_db = MagicMock()
    mock_db.execute.side_effect = OperationalError("connection failure", None, None)

    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        res = client.get("/health/ready")
        assert res.status_code == 503
        assert res.json() == {"status": "unavailable", "database": "disconnected"}
    finally:
        app.dependency_overrides.clear()
