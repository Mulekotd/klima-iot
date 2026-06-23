from fastapi import APIRouter, HTTPException, Query

from app.core.config import settings
from app.schemas.control import (
    ControlCommandCreate,
    ControlCommandHistoryResponse,
    ControlCommandResponse,
    ControlStateRead
)
from app.services.climate import climate_service


router = APIRouter(prefix="/control", tags=["control"])


@router.get("", response_model=ControlStateRead)
async def read_control_state(
    device_id: str = Query(default=settings.default_device_id, min_length=1)
) -> ControlStateRead:
    try:
        return climate_service.get_control_state(device_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("", response_model=ControlCommandResponse)
async def send_control_command(
    command: ControlCommandCreate
) -> ControlCommandResponse:
    return climate_service.apply_control_command(command)


@router.patch("", response_model=ControlCommandResponse)
async def update_control_state(
    command: ControlCommandCreate
) -> ControlCommandResponse:
    return climate_service.apply_control_command(command)


@router.get("/commands", response_model=ControlCommandHistoryResponse)
async def list_control_commands(
    device_id: str = Query(default=settings.default_device_id, min_length=1),
    limit: int = Query(default=20, ge=1, le=100)
) -> ControlCommandHistoryResponse:
    try:
        return climate_service.list_command_history(device_id, limit)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
