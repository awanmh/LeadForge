from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.leads.schemas import LeadCreate
from app.leads.repository import lead_repository
from app.core.logging import logger


class LeadService:
    def process_lead(self, db: Session, lead_in: LeadCreate) -> bool:
        # Check honeypot: if non-empty, silently succeed without DB write (T-02)
        if lead_in.website and lead_in.website.strip():
            logger.info("Honeypot triggered, submission silently discarded without persistence.")
            return False

        try:
            lead_repository.create(db, lead_in)
            logger.info("Valid lead inquiry persisted successfully.")
            return True
        except SQLAlchemyError as exc:
            db.rollback()
            logger.error(f"Database error during lead persistence: {type(exc).__name__}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable. Please try again later."
            ) from exc


lead_service = LeadService()
