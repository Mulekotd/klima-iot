from fastapi import FastAPI
from contextlib import asynccontextmanager
from ORM import Base, engine, async_session
from routers.control import router as control_router
from routers.telemetry import router as telemetry_router

# Para compatibilidade retroativa com scripts ou testes que importem diretamente do simulator:
from schemas import ControlCommand, Telemetry

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas se elas não existirem no Postgres
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Klima Simulator", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registro dos Roteadores sob o prefixo /api
app.include_router(control_router, prefix="/api")
app.include_router(telemetry_router, prefix="/api")

# Dependência get_db exposta para compatibilidade com o conftest.py
from ORM import get_db

@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok"}

# --- Handlers de Exceção Globais ---
import logging
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("klima")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    logger.warning(f"Erro de validação de payload: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Dados enviados são inválidos para o contrato estabelecido.",
            "details": exc.errors()
        }
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc: SQLAlchemyError):
    logger.error(f"Falha de banco de dados no simulador: {str(exc)}")
    return JSONResponse(
        status_code=503,
        content={
            "status": "error",
            "message": "Serviço temporariamente indisponível devido a falha no banco de dados."
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    logger.error(f"Erro não tratado capturado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Ocorreu um erro interno no servidor."
        }
    )
