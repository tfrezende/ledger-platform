import asyncio
import os
from collections.abc import AsyncGenerator, Generator

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from config.settings import get_settings
from infrastructure.db.models import Base


@pytest.fixture(scope="session")
def postgres_url() -> Generator[str, None, None]:
    with PostgresContainer("postgres:16") as pg:
        yield pg.get_connection_url().replace(
            "postgresql+psycopg2", "postgresql+asyncpg"
        )


@pytest.fixture(scope="session")
def redis_url() -> Generator[str, None, None]:
    with RedisContainer("redis:7-alpine") as rc:
        host = rc.get_container_host_ip()
        port = rc.get_exposed_port(6379)
        yield f"redis://{host}:{port}/0"


@pytest.fixture(scope="session")
def patch_settings(postgres_url: str, redis_url: str) -> Generator[None, None, None]:
    os.environ["DATABASE_URL"] = postgres_url
    os.environ["REDIS_URL"] = redis_url
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture(scope="session")
def _create_schema(postgres_url: str, patch_settings: None) -> None:  # noqa: PT004
    engine = create_async_engine(postgres_url)

    async def _setup() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()

    asyncio.run(_setup())


@pytest.fixture(scope="session")
async def client(patch_settings: None, _create_schema: None) -> AsyncGenerator[AsyncClient, None]:
    from main import create_app  # lazy import — env vars must be set first

    app = create_app()
    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app),
            base_url="http://test",
        ) as ac:
            yield ac
