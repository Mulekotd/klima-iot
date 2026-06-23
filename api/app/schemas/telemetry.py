from datetime import datetime

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.core.config import settings


class APIModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class TelemetryCreate(APIModel):
    device_id: str = Field(
        default=settings.default_device_id,
        min_length=1,
        validation_alias=AliasChoices("device_id", "deviceId"),
    )
    current_temperature: float = Field(
        ge=-20,
        le=60,
        validation_alias=AliasChoices(
            "current_temperature",
            "currentTemperature",
            "temperature"
        ),
    )
    current_humidity: float = Field(
        ge=0,
        le=100,
        validation_alias=AliasChoices(
            "current_humidity",
            "currentHumidity",
            "humidity"
        ),
    )
    motion_detected: bool = Field(
        validation_alias=AliasChoices(
            "motion_detected",
            "motionDetected",
            "presence_detected",
            "presenceDetected"
        )
    )
    filter_hours_used: float = Field(
        default=0,
        ge=0,
        validation_alias=AliasChoices("filter_hours_used", "filterHoursUsed")
    )
    compressor_active: bool | None = Field(
        default=None,
        validation_alias=AliasChoices("compressor_active", "compressorActive")
    )
    energy_kwh: float | None = Field(
        default=None,
        ge=0,
        validation_alias=AliasChoices("energy_kwh", "energyKwh")
    )
    recorded_at: datetime | None = None


class TelemetryRead(APIModel):
    device_id: str
    current_temperature: float
    current_humidity: float
    motion_detected: bool
    filter_hours_used: float
    compressor_active: bool | None
    energy_kwh: float | None
    recorded_at: datetime


class TelemetryHistoryResponse(APIModel):
    count: int
    items: list[TelemetryRead]
