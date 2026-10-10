import pytest
from pydantic import ValidationError
from app.leads.schemas import LeadCreate


def test_valid_lead_create():
    lead = LeadCreate(
        name="Jane Doe",
        email="jane@example.com",
        service_slug="web-development",
        message="I would like to discuss a new website project.",
        website="",
    )
    assert lead.name == "Jane Doe"
    assert lead.email == "jane@example.com"
    assert lead.service_slug == "web-development"


def test_invalid_email_raises_validation_error():
    with pytest.raises(ValidationError):
        LeadCreate(
            name="Jane Doe",
            email="not-an-email",
            message="Valid message length here.",
        )


def test_short_name_raises_validation_error():
    with pytest.raises(ValidationError):
        LeadCreate(
            name="J",
            email="jane@example.com",
            message="Valid message length here.",
        )


def test_short_message_raises_validation_error():
    with pytest.raises(ValidationError):
        LeadCreate(
            name="Jane Doe",
            email="jane@example.com",
            message="Too short",
        )


def test_invalid_service_slug_pattern():
    with pytest.raises(ValidationError):
        LeadCreate(
            name="Jane Doe",
            email="jane@example.com",
            service_slug="Invalid Slug!",
            message="Valid message length here.",
        )


def test_extra_fields_forbidden():
    with pytest.raises(ValidationError):
        LeadCreate(
            name="Jane Doe",
            email="jane@example.com",
            message="Valid message length here.",
            extra_field="malicious_payload",  # type: ignore
        )
