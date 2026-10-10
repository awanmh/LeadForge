from sqlalchemy.orm import Session
from app.db.models import Lead
from app.leads.schemas import LeadCreate


class LeadRepository:
    def create(self, db: Session, lead_data: LeadCreate) -> Lead:
        db_lead = Lead(
            name=lead_data.name,
            email=str(lead_data.email).lower(),
            service_slug=lead_data.service_slug,
            message=lead_data.message,
            status="new",
        )
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        return db_lead


lead_repository = LeadRepository()
