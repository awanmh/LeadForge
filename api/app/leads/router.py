from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.leads.schemas import LeadCreate, LeadResponse
from app.leads.service import lead_service
from app.core.security import enforce_rate_limit

router = APIRouter(prefix="/api/v1/leads", tags=["leads"])


@router.post(
    "",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a new lead inquiry",
)
def submit_lead(
    lead_in: LeadCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    enforce_rate_limit(request)
    lead_service.process_lead(db, lead_in)
    return LeadResponse()
