from datetime import datetime
from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator

from app.core.config import settings


ClimateMode = Literal["cool", "fan", "auto", "dry"]
FanSpeed = Literal["auto", "low", "medium", "high"]
CommandSource = Literal["app", "automation", "device", "simulator"]


class APIModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class ControlCommandCreate(APIModel):
    device_id: str = Field(
        default=settings.default_device_id,
        min_length=1,
        validation_alias=AliasChoices("device_id", "deviceId")
    )
    powered: bool | None = Field(
        default=None,
        validation_alias=AliasChoices("powered", "power")
    )
    target_temperature: float | None = Field(
        default=None,
        ge=16,
        le=30,
        validation_alias=AliasChoices("target_temperature", "temperature")
    )
    mode: ClimateMode | None = None
    fan_speed: FanSpeed | None = Field(
        default=None,
        validation_alias=AliasChoices("fan_speed", "fanSpeed")
    )
    eco_enabled: bool | None = Field(
        default=None,
        validation_alias=AliasChoices("eco_enabled", "eco")
    )
    timer_enabled: bool | None = Field(
        default=None,
        validation_alias=AliasChoices("timer_enabled", "timer")
    )
    timer_minutes: int | None = Field(default=None, ge=0, le=1440)
    reset_filter: bool = False
    source: CommandSource = "app"

    @field_validator("mode", mode="before")
    @classmethod
    def normalize_mode(cls, value: object) -> object:
        if value is None:
            return value

        normalized = str(value).strip().lower()
        mode_map = {
            "resfriar": "cool",
            "cooling": "cool",
            "ventilar": "fan",
            "ventilacao": "fan",
            "ventilação": "fan",
            "automatico": "auto",
            "automático": "auto",
            "desumidificar": "dry"
        }
        return mode_map.get(normalized, normalized)

    @field_validator("fan_speed", mode="before")
    @classmethod
    def normalize_fan_speed(cls, value: object) -> object:
        if value is None:
            return value

        normalized = str(value).strip().lower()
        speed_map = {
            "baixa": "low",
            "low": "low",
            "media": "medium",
            "média": "medium",
            "medium": "medium",
            "alta": "high",
            "high": "high"
        }
        return speed_map.get(normalized, normalized)


class ControlStateRead(APIModel):
    device_id: str
    powered: bool
    target_temperature: float
    mode: ClimateMode
    fan_speed: FanSpeed
    eco_enabled: bool
    timer_enabled: bool
    timer_minutes: int | None
    last_command_id: str | None
    updated_at: datetime


class ControlCommandResponse(APIModel):
    status: Literal["success"] = "success"
    delivery_status: Literal["accepted"] = "accepted"
    command_id: str
    queued_at: datetime
    command_registered: ControlStateRead
    state: ControlStateRead
    message: str


class ControlCommandHistoryItem(APIModel):
    command_id: str
    device_id: str
    source: CommandSource
    status: Literal["accepted", "delivered", "failed"]
    requested_state: ControlStateRead
    created_at: datetime


class ControlCommandHistoryResponse(APIModel):
    count: int
    items: list[ControlCommandHistoryItem]
