from dataclasses import dataclass
from datetime import datetime, timezone
from threading import RLock

from app.core.config import settings
from app.schemas.control import (
    ControlCommandCreate,
    ControlCommandHistoryItem,
    ControlCommandHistoryResponse,
    ControlCommandResponse,
    ControlStateRead
)
from app.schemas.device import DeviceRead
from app.schemas.telemetry import TelemetryCreate, TelemetryHistoryResponse, TelemetryRead
from app.services.snowflake import snowflake_ids


@dataclass
class DeviceMetadata:
    id: str
    name: str
    room: str
    model: str
    online: bool
    last_seen_at: datetime | None


def _now() -> datetime:
    return datetime.now(timezone.utc)


class ClimateService:
    def __init__(self) -> None:
        self._lock = RLock()
        self._devices: dict[str, DeviceMetadata] = {}
        self._control_states: dict[str, ControlStateRead] = {}
        self._latest_telemetry: dict[str, TelemetryRead] = {}
        self._telemetry_history: list[TelemetryRead] = []
        self._command_history: list[ControlCommandHistoryItem] = []
        self._seed_default_device()

    def get_latest_telemetry(self, device_id: str) -> TelemetryRead:
        with self._lock:
            self._require_device(device_id)
            return self._latest_telemetry[device_id]

    def register_telemetry(self, payload: TelemetryCreate) -> TelemetryRead:
        with self._lock:
            self._ensure_device(payload.device_id)
            recorded_at = payload.recorded_at or _now()
            telemetry = TelemetryRead(
                device_id=payload.device_id,
                current_temperature=payload.current_temperature,
                current_humidity=payload.current_humidity,
                motion_detected=payload.motion_detected,
                filter_hours_used=payload.filter_hours_used,
                compressor_active=payload.compressor_active,
                energy_kwh=payload.energy_kwh,
                recorded_at=recorded_at
            )

            self._latest_telemetry[payload.device_id] = telemetry
            self._telemetry_history.append(telemetry)
            self._telemetry_history = self._telemetry_history[
                -settings.telemetry_history_limit :
            ]

            device = self._devices[payload.device_id]
            device.online = True
            device.last_seen_at = recorded_at

            return telemetry

    def list_telemetry_history(
        self,
        device_id: str,
        limit: int
    ) -> TelemetryHistoryResponse:
        with self._lock:
            self._require_device(device_id)
            items = [
                item
                for item in reversed(self._telemetry_history)
                if item.device_id == device_id
            ][:limit]
            return TelemetryHistoryResponse(count=len(items), items=items)

    def get_control_state(self, device_id: str) -> ControlStateRead:
        with self._lock:
            self._require_device(device_id)
            return self._control_states[device_id]

    def apply_control_command(
        self,
        payload: ControlCommandCreate
    ) -> ControlCommandResponse:
        with self._lock:
            self._ensure_device(payload.device_id)

            queued_at = _now()
            command_id = snowflake_ids.generate(payload.device_id, queued_at)
            current_state = self._control_states[payload.device_id]
            update_data = current_state.model_dump()
            update_data.update(
                {
                    "last_command_id": command_id,
                    "updated_at": queued_at
                }
            )

            if payload.powered is not None:
                update_data["powered"] = payload.powered
            if payload.target_temperature is not None:
                update_data["target_temperature"] = payload.target_temperature
            if payload.mode is not None:
                update_data["mode"] = payload.mode
            if payload.fan_speed is not None:
                update_data["fan_speed"] = payload.fan_speed
            if payload.eco_enabled is not None:
                update_data["eco_enabled"] = payload.eco_enabled
            if payload.timer_enabled is not None:
                update_data["timer_enabled"] = payload.timer_enabled
                if payload.timer_enabled and update_data["timer_minutes"] is None:
                    update_data["timer_minutes"] = 120
                if not payload.timer_enabled:
                    update_data["timer_minutes"] = None
            if payload.timer_minutes is not None:
                update_data["timer_minutes"] = payload.timer_minutes or None
                update_data["timer_enabled"] = payload.timer_minutes > 0

            next_state = ControlStateRead(**update_data)
            self._control_states[payload.device_id] = next_state

            if payload.reset_filter:
                self._reset_filter_counter(payload.device_id, queued_at)

            history_item = ControlCommandHistoryItem(
                command_id=command_id,
                device_id=payload.device_id,
                source=payload.source,
                status="accepted",
                requested_state=next_state,
                created_at=queued_at
            )
            self._command_history.append(history_item)
            self._command_history = self._command_history[
                -settings.command_history_limit :
            ]

            return ControlCommandResponse(
                command_id=command_id,
                queued_at=queued_at,
                command_registered=next_state,
                state=next_state,
                message="Command accepted for delivery to the air conditioner."
            )

    def list_command_history(
        self,
        device_id: str,
        limit: int
    ) -> ControlCommandHistoryResponse:
        with self._lock:
            self._require_device(device_id)
            items = [
                item
                for item in reversed(self._command_history)
                if item.device_id == device_id
            ][:limit]
            return ControlCommandHistoryResponse(count=len(items), items=items)

    def list_devices(self) -> list[DeviceRead]:
        with self._lock:
            return [self._build_device_read(device_id) for device_id in self._devices]

    def get_device(self, device_id: str) -> DeviceRead:
        with self._lock:
            self._require_device(device_id)
            return self._build_device_read(device_id)

    def _seed_default_device(self) -> None:
        device_id = settings.default_device_id
        now = _now()
        self._devices[device_id] = DeviceMetadata(
            id=device_id,
            name="Samsung WindFree",
            room="Sala de estar",
            model="Smart AC retrofit",
            online=True,
            last_seen_at=now
        )
        self._control_states[device_id] = self._default_control_state(device_id, now)
        telemetry = TelemetryRead(
            device_id=device_id,
            current_temperature=24.3,
            current_humidity=58.0,
            motion_detected=True,
            filter_hours_used=46.0,
            compressor_active=True,
            energy_kwh=4.2,
            recorded_at=now
        )
        self._latest_telemetry[device_id] = telemetry
        self._telemetry_history.append(telemetry)

    def _ensure_device(self, device_id: str) -> None:
        if device_id in self._devices:
            return

        now = _now()
        self._devices[device_id] = DeviceMetadata(
            id=device_id,
            name=device_id.replace("-", " ").title(),
            room="Ambiente",
            model="Klima device",
            online=True,
            last_seen_at=now
        )
        self._control_states[device_id] = self._default_control_state(device_id, now)
        self._latest_telemetry[device_id] = TelemetryRead(
            device_id=device_id,
            current_temperature=24.0,
            current_humidity=60.0,
            motion_detected=False,
            filter_hours_used=0.0,
            compressor_active=False,
            energy_kwh=None,
            recorded_at=now
        )

    def _require_device(self, device_id: str) -> None:
        if device_id not in self._devices:
            raise KeyError(f"Device '{device_id}' was not found.")

    def _default_control_state(
        self,
        device_id: str,
        updated_at: datetime
    ) -> ControlStateRead:
        return ControlStateRead(
            device_id=device_id,
            powered=True,
            target_temperature=22.0,
            mode="cool",
            fan_speed="auto",
            eco_enabled=True,
            timer_enabled=False,
            timer_minutes=None,
            last_command_id=None,
            updated_at=updated_at
        )

    def _reset_filter_counter(self, device_id: str, recorded_at: datetime) -> None:
        latest = self._latest_telemetry[device_id]
        reset_telemetry = latest.model_copy(
            update={
                "filter_hours_used": 0.0,
                "recorded_at": recorded_at
            }
        )
        self._latest_telemetry[device_id] = reset_telemetry
        self._telemetry_history.append(reset_telemetry)
        self._telemetry_history = self._telemetry_history[
            -settings.telemetry_history_limit :
        ]

    def _build_device_read(self, device_id: str) -> DeviceRead:
        metadata = self._devices[device_id]
        state = self._control_states[device_id]
        telemetry = self._latest_telemetry.get(device_id)
        return DeviceRead(
            id=metadata.id,
            name=metadata.name,
            room=metadata.room,
            model=metadata.model,
            online=metadata.online,
            last_seen_at=metadata.last_seen_at,
            powered=state.powered,
            target_temperature=state.target_temperature,
            current_temperature=telemetry.current_temperature if telemetry else None,
            current_humidity=telemetry.current_humidity if telemetry else None
        )


climate_service = ClimateService()
