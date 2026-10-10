# LeadForge API

Private lead intake and validation API built with FastAPI, SQLAlchemy 2.0, and PostgreSQL.

## Features
- Input validation with Pydantic 2
- Honeypot spam filtering
- Rate limiting and body size protection
- Health checks: `/health/live` and `/health/ready`
- Private persistence in `leadforge_app` database
