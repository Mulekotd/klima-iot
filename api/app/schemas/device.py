from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DeviceRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    room: str
    model: str
    online: bool
    last_seen_at: datetime | None
    powered: bool
    target_temperature: float
    current_temperature: float | None
    current_humidity: float | None
