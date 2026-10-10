import uuid
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.leads.router import router as leads_router
from app.health.router import router as health_router

app = FastAPI(
    title="LeadForge Private Lead Intake API",
    version="1.0.0",
    docs_url="/docs" if settings.app_env == "development" else None,
    redoc_url=None,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.app_env == "development" else [settings.trusted_proxies],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    # Request Correlation ID
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    request.state.request_id = request_id

    # Enforce request body size limit
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > settings.max_request_bytes:
        return JSONResponse(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={"detail": "Payload too large. Maximum size exceeded."},
            headers={"X-Request-ID": request_id},
        )

    response: Response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Safe validation response that doesn't leak internal paths or raw sensitive user values
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"] if loc != "body")
        errors.append({
            "field": field,
            "message": err["msg"],
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": errors},
    )


app.include_router(health_router)
app.include_router(leads_router)
