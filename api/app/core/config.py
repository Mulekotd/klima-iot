from dataclasses import dataclass, field
import os


def _csv_env(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    raw_value = os.getenv(name)
    if not raw_value:
        return default

    values = tuple(item.strip() for item in raw_value.split(",") if item.strip())
    return values or default


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


settings = Settings()
