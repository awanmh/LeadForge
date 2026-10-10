import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    CheckConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), nullable=False)
    email = Column(String(254), nullable=False)
    service_slug = Column(String(120), nullable=True)
    message = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="new")
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('new', 'contacted', 'closed')",
            name="check_lead_status",
        ),
        Index("ix_leads_created_at", created_at.desc()),
    )
