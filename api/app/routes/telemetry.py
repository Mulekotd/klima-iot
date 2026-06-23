from fastapi import APIRouter, HTTPException, Query, status

from app.core.config import settings
from app.schemas.telemetry import (
    TelemetryCreate,
    TelemetryHistoryResponse,
    TelemetryRead
)
from app.services.climate import climate_service


router = APIRouter(prefix="/telemetry", tags=["telemetry"])


@router.get("", response_model=TelemetryRead)
async def read_latest_telemetry(
    device_id: str = Query(default=settings.default_device_id, min_length=1)
) -> TelemetryRead:
    try:
        return climate_service.get_latest_telemetry(device_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("", response_model=TelemetryRead, status_code=status.HTTP_201_CREATED)
async def ingest_telemetry(payload: TelemetryCreate) -> TelemetryRead:
    return climate_service.register_telemetry(payload)


@router.get("/history", response_model=TelemetryHistoryResponse)
async def read_telemetry_history(
    device_id: str = Query(default=settings.default_device_id, min_length=1),
    limit: int = Query(default=20, ge=1, le=100)
) -> TelemetryHistoryResponse:
    try:
        return climate_service.list_telemetry_history(device_id, limit)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
