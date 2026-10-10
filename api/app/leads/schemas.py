from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class LeadCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr = Field(..., max_length=254)
    service_slug: Optional[str] = Field(
        default=None,
        max_length=120,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )
    message: str = Field(..., min_length=10, max_length=5000)
    website: Optional[str] = Field(default="", max_length=500)

    model_config = ConfigDict(extra="forbid")

    @field_validator("name", "message")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Field cannot be empty or whitespace only")
        return trimmed


class LeadResponse(BaseModel):
    message: str = "Inquiry received."
