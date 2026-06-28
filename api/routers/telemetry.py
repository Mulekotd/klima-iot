import asyncio
import os
import random
from fastapi import APIRouter, HTTPException, Depends
from ORM import get_db
from schemas import Telemetry
from repositories.telemetry import TelemetryRepository

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

off_sensors = False  # Simula problema nos Sensores

# Flag para desativar os sleeps de rede local durante os testes
TESTING = os.getenv("TESTING", "false").lower() == "true"

async def get_telemetry_repo(db = Depends(get_db)) -> TelemetryRepository:
    return TelemetryRepository(db)

@router.get("", response_model=Telemetry)
async def read_sensors(repo: TelemetryRepository = Depends(get_telemetry_repo)):
    if not TESTING:
        # Simula o tempo de processamento do microcontrolador
        await asyncio.sleep(random.uniform(0.2, 2))
    
    # Gera dados de temperatura com pequenas flutuações
    temperature = 22.0 + random.uniform(-0.5, 0.5)
    
    # Injeção de falha: sensores offline
    if off_sensors:
         raise HTTPException(status_code=504, detail="Gateway Timeout - Sensors did not respond")

    # Cria objeto Pydantic de resposta
    telemetry_data = Telemetry(
        current_temperature=temperature,
        current_humidity=65.5 + random.uniform(-2.0, 2.0),
        motion_detected=random.choice([True, False]),
        filter_hours_used=random.uniform(15.0, 150.0)
    )

    # Gravação delegada ao Repositório (Desacoplamento Clean Architecture)
    await repo.create(telemetry_data)

    return telemetry_data
