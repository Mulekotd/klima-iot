from fastapi import APIRouter, HTTPException

from app.schemas.device import DeviceRead
from app.services.climate import climate_service


router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("", response_model=list[DeviceRead])
async def list_devices() -> list[DeviceRead]:
    return climate_service.list_devices()


@router.get("/{device_id}", response_model=DeviceRead)
async def read_device(device_id: str) -> DeviceRead:
    try:
        return climate_service.get_device(device_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
