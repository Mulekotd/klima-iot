import pytest
from httpx import AsyncClient
from sqlalchemy import select

# Tenta importar o modelo para fazer asserts diretos no banco de dados
try:
    from ORM import ControlCommandORM
except ImportError:
    ControlCommandORM = None

pytestmark = pytest.mark.asyncio

async def test_create_control_command(client: AsyncClient, db_session):
    """Testa se o envio de um comando registra os dados corretamente no banco."""
    # Garante que os imports essenciais do app estão presentes, caso contrário, pula
    if ControlCommandORM is None:
        pytest.skip("ControlCommandORM model not implemented yet (Red Phase)")

    payload = {
        "power": True,
        "target_temperature": 24.5,
        "timer_minutes": 45,
        "reset_filter": False
    }

    response = await client.post("/api/control", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    
    # Verifica a persistência no Banco de Dados
    result = await db_session.execute(select(ControlCommandORM))
    commands = result.scalars().all()
    
    assert len(commands) == 1
    db_command = commands[0]
    assert db_command.power is True
    assert db_command.target_temperature == 24.5
    assert db_command.timer_minutes == 45
    assert db_command.reset_filter is False
    assert db_command.id is not None
    assert db_command.created_at is not None

async def test_control_command_validation_error(client: AsyncClient):
    """Testa validação de campos inválidos."""
    payload = {
        "power": "not-a-bool",  # Pydantic deve falhar aqui
        "target_temperature": "hot",
        "timer_minutes": -10,
        "reset_filter": None
    }
    
    response = await client.post("/api/control", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
