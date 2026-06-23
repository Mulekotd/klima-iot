from dataclasses import dataclass, field
import os


def _bool_env(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


def _csv_env(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    raw_value = os.getenv(name)
    if not raw_value:
        return default

    values = tuple(item.strip() for item in raw_value.split(",") if item.strip())
    return values or default


def _int_env(name: str, default: int, minimum: int | None = None) -> int:
    raw_value = os.getenv(name)
    if not raw_value:
        return default

    try:
        value = int(raw_value)
    except ValueError:
        return default

    if minimum is not None:
        return max(value, minimum)
    return value


@dataclass(frozen=True)
class Settings:
    app_name: str = "Klima API"
    version: str = "0.1.0"
    api_prefix: str = os.getenv("API_PREFIX", "/api")
    default_device_id: str = os.getenv("DEFAULT_DEVICE_ID", "living-room-ac")
    telemetry_history_limit: int = int(os.getenv("TELEMETRY_HISTORY_LIMIT", "100"))
    command_history_limit: int = int(os.getenv("COMMAND_HISTORY_LIMIT", "100"))
    cors_origins: tuple[str, ...] = field(
        default_factory=lambda: _csv_env(
            "CORS_ORIGINS",
            (
                "http://localhost:3000",
                "http://127.0.0.1:3000"
            ),
        )
    )
    cors_allow_credentials: bool = _bool_env("CORS_ALLOW_CREDENTIALS", True)
    cors_allow_methods: tuple[str, ...] = field(
        default_factory=lambda: _csv_env(
            "CORS_ALLOW_METHODS",
            ("GET", "POST", "PATCH", "OPTIONS"),
        )
    )
    cors_allow_headers: tuple[str, ...] = field(
        default_factory=lambda: _csv_env("CORS_ALLOW_HEADERS", ("*",))
    )
    security_headers_enabled: bool = _bool_env("SECURITY_HEADERS_ENABLED", True)
    security_hsts_enabled: bool = _bool_env("SECURITY_HSTS_ENABLED", True)
    security_hsts_max_age: int = _int_env(
        "SECURITY_HSTS_MAX_AGE",
        31_536_000,
        minimum=0,
    )
    rate_limit_enabled: bool = _bool_env("RATE_LIMIT_ENABLED", True)
    rate_limit_requests: int = _int_env("RATE_LIMIT_REQUESTS", 120, minimum=1)
    rate_limit_window_seconds: int = _int_env(
        "RATE_LIMIT_WINDOW_SECONDS",
        60,
        minimum=1,
    )
    rate_limit_exempt_paths: tuple[str, ...] = field(
        default_factory=lambda: _csv_env("RATE_LIMIT_EXEMPT_PATHS", ("/health",))
    )
    rate_limit_trust_proxy_headers: bool = _bool_env(
        "RATE_LIMIT_TRUST_PROXY_HEADERS",
        False,
    )


settings = Settings()
