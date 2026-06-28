import asyncio
import os
import random
from fastapi import APIRouter, HTTPException, Depends
from ORM import get_db
from schemas import ControlCommand
from repositories.control import ControlRepository

router = APIRouter(prefix="/control", tags=["Control"])

off_hardware = False  # Simula problema no Hardware

# Flag para desativar os sleeps de rede local durante os testes
TESTING = os.getenv("TESTING", "false").lower() == "true"

async def get_control_repo(db = Depends(get_db)) -> ControlRepository:
    return ControlRepository(db)

@router.post("")
async def send_command(
    command: ControlCommand, 
    repo: ControlRepository = Depends(get_control_repo)
):
    if not TESTING:
        # Simula o tempo de resposta da rede local (0.2s a 2s)
        await asyncio.sleep(random.uniform(0.2, 2))
    
    # Injeção de falha: hardware offline
    if off_hardware:
        raise HTTPException(status_code=504, detail="Gateway Timeout - Hardware did not respond")

    # Gravação delegada ao Repositório (Desacoplamento Clean Architecture)
    await repo.create(command)

    return {"status": "success", "command_registered": command}

