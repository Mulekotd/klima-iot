import os
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Float, Boolean, Integer, DateTime, func

# Configuração da URL de conexão PostgreSQL + asyncpg
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")  # 'database' dentro do docker
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "klima")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Criação do engine assíncrono para PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Classe Base declarativa do SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass

class ControlCommandORM(Base):
    __tablename__ = "control_commands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    power: Mapped[bool] = mapped_column(Boolean, nullable=False)
    target_temperature: Mapped[float] = mapped_column(Float, nullable=False)
    timer_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    reset_filter: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )

class TelemetryORM(Base):
    __tablename__ = "telemetry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    current_temperature: Mapped[float] = mapped_column(Float, nullable=False)
    current_humidity: Mapped[float] = mapped_column(Float, nullable=False)
    motion_detected: Mapped[bool] = mapped_column(Boolean, nullable=False)
    filter_hours_used: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )

async def get_db():
    async with async_session() as session:
        yield session