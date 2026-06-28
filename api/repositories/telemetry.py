from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ORM import TelemetryORM
from schemas import Telemetry

class TelemetryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, telemetry: Telemetry) -> TelemetryORM:
        db_telemetry = TelemetryORM(
            current_temperature=telemetry.current_temperature,
            current_humidity=telemetry.current_humidity,
            motion_detected=telemetry.motion_detected,
            filter_hours_used=telemetry.filter_hours_used
        )
        self.db.add(db_telemetry)
        await self.db.commit()
        await self.db.refresh(db_telemetry)
        return db_telemetry

    async def get_all(self, limit: int = 100) -> list[TelemetryORM]:
        result = await self.db.execute(
            select(TelemetryORM).order_by(TelemetryORM.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())
