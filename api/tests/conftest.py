import asyncio
import os

os.environ["TESTING"] = "true"

import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Importa a app e o Base do ORM (serão criados na fase Green)
# Se os arquivos ainda não existirem ou não tiverem as classes, tratamos o ImportError para não quebrar a suíte.
try:
    from simulator import app
    from ORM import get_db
except ImportError:
    app = None
    get_db = None

try:
    from ORM import Base
except ImportError:
    Base = None

# Configura URL do banco de teste. Prioriza env variable.
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", 
    "sqlite+aiosqlite:///:memory:"  # Fallback padrão para testes rápidos sem depender de infra local externa
)

@pytest.fixture(scope="session")
def event_loop():
    """Garante que o event loop do asyncio tenha escopo de sessão."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    """Cria o engine assíncrono para os testes."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="session")
async def setup_db(test_engine):
    """Cria a estrutura das tabelas no banco de testes e limpa ao final."""
    if Base is not None:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    if Base is not None:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(test_engine, setup_db) -> AsyncGenerator[AsyncSession, None]:
    """Fornece uma sessão assíncrona com rollback automático para manter cada teste isolado."""
    testing_session_local = async_sessionmaker(
        bind=test_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with testing_session_local() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """Cria um cliente HTTP assíncrono injetando a sessão de teste no FastAPI."""
    if app is None or get_db is None:
        # Fallback se a app ainda não estiver pronta (fase Red inicial)
        from fastapi import FastAPI
        temp_app = FastAPI()
        async with AsyncClient(transport=ASGITransport(app=temp_app), base_url="http://test") as ac:
            yield ac
    else:
        # Override da dependência get_db do FastAPI para usar a sessão do teste
        async def override_get_db():
            yield db_session

        app.dependency_overrides[get_db] = override_get_db
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            yield ac
        app.dependency_overrides.clear()
