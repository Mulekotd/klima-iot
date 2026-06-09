from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import random

app = FastAPI(title="Klima simulator")

off_hardware = False # Simula problema no Hardware
off_sensors = False  # Simula problema nos Sensores

# Dados do frontend
class ControlCommand(BaseModel):
    power: bool
    target_temperature: float
    timer_minutes: int  # Tempo para o ar-condicionado desligar
    reset_filter: bool  # Redefinir tempo após limpeza do filtro
    
# Dados do Hardware
class Telemetry(BaseModel):
    current_temperature: float
    current_humidity: float
    motion_detected: bool
    filter_hours_used: float


@app.post("/api/control")
async def send_command(command: ControlCommand):
    # Simula o tempo de resposta da rede local (0.2s a 2s)
    await asyncio.sleep(random.uniform(0.2, 2))
    
    # Injeção de falha: 20% de chance de simular hardware offline
    if off_hardware:
        raise HTTPException(status_code=504, detail="Gateway Timeout - Hardware did not respond")

    return {"status": "success", "command_registered": command}



@app.get("/api/telemetry", response_model=Telemetry)
async def read_sensors():
    # Simula o tempo de processamento do microcontrolador
    await asyncio.sleep(random.uniform(0.2, 2))
    
    # Gera dados de temperatura com pequenas flutuações
    temperature = 22.0 + random.uniform(-0.5, 0.5)
    
    # Injeção de falha: 20% de chance do sensor de temperatura falhar (retorna NaN)
    if off_sensors:
         raise HTTPException(status_code=504, detail="Gateway Timeout - Sensors did not respond")

    return Telemetry(
        current_temperature=temperature,
        current_humidity=65.5 + random.uniform(-2.0, 2.0),
        motion_detected=random.choice([True, False]),
        filter_hours_used= random.uniform(15.0,150.0)
    )