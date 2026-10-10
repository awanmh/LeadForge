from fastapi import APIRouter, Depends, status, Response
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", status_code=status.HTTP_200_OK)
def liveness():
    return {"status": "live"}


@router.get("/ready")
def readiness(response: Response, db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unavailable", "database": "disconnected"}
