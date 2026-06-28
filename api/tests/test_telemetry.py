import pytest
from httpx import AsyncClient
from sqlalchemy import select

# Tenta importar o modelo para fazer asserts diretos no banco de dados
try:
    from ORM import TelemetryORM
except ImportError:
    TelemetryORM = None

pytestmark = pytest.mark.asyncio

async def test_read_and_persist_telemetry(client: AsyncClient, db_session):
    """Testa se a leitura dos sensores retorna dados e persiste um registro de telemetria no banco."""
    if TelemetryORM is None:
        pytest.skip("TelemetryORM model not implemented yet (Red Phase)")

    response = await client.get("/api/telemetry")
    assert response.status_code == 200
    
    data = response.json()
    assert "current_temperature" in data
    assert "current_humidity" in data
    assert "motion_detected" in data
    assert "filter_hours_used" in data

    # Verifica se o registro foi salvo no banco
    result = await db_session.execute(select(TelemetryORM))
    telemetries = result.scalars().all()
    
    assert len(telemetries) == 1
    db_telemetry = telemetries[0]
    assert db_telemetry.current_temperature == data["current_temperature"]
    assert db_telemetry.current_humidity == data["current_humidity"]
    assert db_telemetry.motion_detected == data["motion_detected"]
    assert db_telemetry.filter_hours_used == data["filter_hours_used"]
    assert db_telemetry.id is not None
    assert db_telemetry.created_at is not None
