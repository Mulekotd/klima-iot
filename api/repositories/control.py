from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ORM import ControlCommandORM
from schemas import ControlCommand

class ControlRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, command: ControlCommand) -> ControlCommandORM:
        db_command = ControlCommandORM(
            power=command.power,
            target_temperature=command.target_temperature,
            timer_minutes=command.timer_minutes,
            reset_filter=command.reset_filter
        )
        self.db.add(db_command)
        await self.db.commit()
        await self.db.refresh(db_command)
        return db_command

    async def get_latest(self) -> ControlCommandORM | None:
        result = await self.db.execute(
            select(ControlCommandORM).order_by(ControlCommandORM.created_at.desc()).limit(1)
        )
        return result.scalars().first()
