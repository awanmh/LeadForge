import time
from collections import defaultdict
from fastapi import Request, HTTPException, status
from app.core.config import settings


class RateLimiter:
    def __init__(self, requests_per_minute: int = 10):
        self.rate_limit = requests_per_minute
        self.requests: dict[str, list[float]] = defaultdict(list)

    def is_rate_limited(self, client_ip: str) -> bool:
        now = time.time()
        window_start = now - 60.0

        # Purge older timestamps for this IP
        self.requests[client_ip] = [
            ts for ts in self.requests[client_ip] if ts > window_start
        ]

        if len(self.requests[client_ip]) >= self.rate_limit:
            return True

        self.requests[client_ip].append(now)
        return False


rate_limiter = RateLimiter(requests_per_minute=settings.rate_limit_per_minute)


def get_client_ip(request: Request) -> str:
    # If request comes from trusted proxy, check X-Forwarded-For or X-Real-IP
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        # Take the leftmost untrusted IP or first IP
        return forwarded.split(",")[0].strip()

    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()

    if request.client:
        return request.client.host
    return "127.0.0.1"


def enforce_rate_limit(request: Request):
    client_ip = get_client_ip(request)
    if rate_limiter.is_rate_limited(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later."
        )
