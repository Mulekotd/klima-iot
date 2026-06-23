from fastapi import FastAPI

from app.core.config import settings
from app.core.security import configure_security
from app.routes import control, devices, telemetry


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description="Backend API for Klima IoT air conditioner telemetry and control.",
    )

    configure_security(app)

    @app.get("/health", tags=["health"], summary="Application health check")
    async def health_check() -> dict[str, str]:
        return {
            "status": "ok",
            "service": settings.app_name,
            "version": settings.version,
        }

    @app.get("/", include_in_schema=False)
    async def root() -> dict[str, str]:
        return {
            "name": settings.app_name,
            "status": "ok",
            "docs": "/docs",
            "health": "/health",
        }

    app.include_router(telemetry.router, prefix=settings.api_prefix)
    app.include_router(control.router, prefix=settings.api_prefix)
    app.include_router(devices.router, prefix=settings.api_prefix)

    return app


app = create_app()
