import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.core.database import Base
from app.dependecies import get_db
from app.core.config import settings
from app.core.redis_client import get_redis_client
import redis.asyncio as redis
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):

    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    TestingSessionLocal = async_sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine
    )

    async with TestingSessionLocal() as session:
        yield session

    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_client(db_session):

    async def override_get_db():
        yield db_session

    async def override_get_redis():
        client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True,
        )

        await client.flushdb()

        try:
            yield client
        finally:
            await client.aclose()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis_client] = override_get_redis

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()
