import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from app.main import app
from app.db.session import SessionLocal
from app.core.security import rate_limiter


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_leads_table():
    rate_limiter.requests.clear()
    db = SessionLocal()
    try:
        db.execute(text("TRUNCATE TABLE leads RESTART IDENTITY CASCADE"))
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()
    yield
    rate_limiter.requests.clear()
