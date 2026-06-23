from dataclasses import dataclass
from math import ceil
from threading import Lock
from time import monotonic, time
from typing import Any, Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from app.core.config import settings


SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; "
        "base-uri 'self'; "
        "connect-src 'self'; "
        "font-src 'self' https://cdn.jsdelivr.net data:; "
        "form-action 'self'; "
        "frame-ancestors 'none'; "
        "img-src 'self' data: https://fastapi.tiangolo.com; "
        "object-src 'none'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net"
    ),
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Resource-Policy": "same-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Referrer-Policy": "no-referrer",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "0",
}


@dataclass
class _RateLimitWindow:
    count: int
    reset_at: float


@dataclass(frozen=True)
class _RateLimitDecision:
    allowed: bool
    remaining: int
    reset_at: float
    retry_after: int


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: Any,
        *,
        hsts_enabled: bool,
        hsts_max_age: int,
    ) -> None:
        super().__init__(app)
        self.hsts_enabled = hsts_enabled
        self.hsts_max_age = hsts_max_age

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        response = await call_next(request)

        for header, value in SECURITY_HEADERS.items():
            if header not in response.headers:
                response.headers[header] = value

        if self._should_add_hsts(request):
            response.headers["Strict-Transport-Security"] = (
                f"max-age={self.hsts_max_age}; includeSubDomains"
            )

        return response

    def _should_add_hsts(self, request: Request) -> bool:
        if not self.hsts_enabled or self.hsts_max_age <= 0:
            return False

        forwarded_proto = request.headers.get("x-forwarded-proto", "")
        proto = forwarded_proto.split(",", maxsplit=1)[0].strip().lower()
        return proto == "https" or request.url.scheme == "https"


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: Any,
        *,
        limit: int,
        window_seconds: int,
        exempt_paths: tuple[str, ...],
        trust_proxy_headers: bool,
    ) -> None:
        super().__init__(app)
        self.limit = max(limit, 1)
        self.window_seconds = max(window_seconds, 1)
        self.exempt_paths = {self._normalize_path(path) for path in exempt_paths}
        self.trust_proxy_headers = trust_proxy_headers
        self._lock = Lock()
        self._last_prune_at = 0.0
        self._windows: dict[str, _RateLimitWindow] = {}

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if request.method == "OPTIONS" or self._is_exempt(request.url.path):
            return await call_next(request)

        decision = self._check_limit(self._client_identifier(request))
        rate_headers = self._rate_limit_headers(decision)

        if not decision.allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded."},
                headers={
                    **rate_headers,
                    "Retry-After": str(decision.retry_after),
                },
            )

        response = await call_next(request)
        response.headers.update(rate_headers)
        return response

    def _check_limit(self, identifier: str) -> _RateLimitDecision:
        now = monotonic()

        with self._lock:
            window = self._windows.get(identifier)
            if window is None or window.reset_at <= now:
                window = _RateLimitWindow(count=1, reset_at=now + self.window_seconds)
                self._windows[identifier] = window
                self._prune_expired_windows(now)
                return self._decision(True, window, now)

            if window.count >= self.limit:
                return self._decision(False, window, now)

            window.count += 1
            return self._decision(True, window, now)

    def _decision(
        self,
        allowed: bool,
        window: _RateLimitWindow,
        checked_at: float,
    ) -> _RateLimitDecision:
        retry_after = max(ceil(window.reset_at - checked_at), 0)
        return _RateLimitDecision(
            allowed=allowed,
            remaining=max(self.limit - window.count, 0),
            reset_at=time() + retry_after,
            retry_after=retry_after,
        )

    def _client_identifier(self, request: Request) -> str:
        if self.trust_proxy_headers:
            forwarded_for = request.headers.get("x-forwarded-for")
            if forwarded_for:
                return forwarded_for.split(",", maxsplit=1)[0].strip()

        if request.client is None:
            return "anonymous"

        return request.client.host

    def _is_exempt(self, path: str) -> bool:
        return self._normalize_path(path) in self.exempt_paths

    def _normalize_path(self, path: str) -> str:
        normalized = path.strip() or "/"
        if normalized != "/":
            normalized = normalized.rstrip("/")
        return normalized

    def _prune_expired_windows(self, now: float) -> None:
        if now - self._last_prune_at < self.window_seconds:
            return

        self._last_prune_at = now
        expired_identifiers = [
            identifier
            for identifier, window in self._windows.items()
            if window.reset_at <= now
        ]
        for identifier in expired_identifiers:
            del self._windows[identifier]

    def _rate_limit_headers(self, decision: _RateLimitDecision) -> dict[str, str]:
        return {
            "X-RateLimit-Limit": str(self.limit),
            "X-RateLimit-Remaining": str(decision.remaining),
            "X-RateLimit-Reset": str(int(decision.reset_at)),
        }


def configure_security(app: FastAPI) -> None:
    if settings.rate_limit_enabled:
        app.add_middleware(
            RateLimitMiddleware,
            limit=settings.rate_limit_requests,
            window_seconds=settings.rate_limit_window_seconds,
            exempt_paths=settings.rate_limit_exempt_paths,
            trust_proxy_headers=settings.rate_limit_trust_proxy_headers,
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=list(settings.cors_allow_methods),
        allow_headers=list(settings.cors_allow_headers),
    )

    if settings.security_headers_enabled:
        app.add_middleware(
            SecurityHeadersMiddleware,
            hsts_enabled=settings.security_hsts_enabled,
            hsts_max_age=settings.security_hsts_max_age,
        )
