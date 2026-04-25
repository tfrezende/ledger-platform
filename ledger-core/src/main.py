import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from api.v1.health import router as health_router
from api.v1.owners import router as owners_router
from api.v1.accounts import router as accounts_router
from config.settings import get_settings
from infrastructure.cache.redis_client import create_redis_client
from infrastructure.db.session import create_session_factory


def configure_logging() -> None:
    settings = get_settings()

    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if settings.app_env == "development":
        renderer: structlog.types.Processor = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[*shared_processors, structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[structlog.stdlib.ProcessorFormatter.remove_processors_meta, renderer],
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(settings.log_level.upper())


configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = get_settings()

    engine = create_async_engine(
        str(settings.database_url),
        pool_size=10,
        max_overflow=5,
        echo=False,
    )

    app.state.db_engine = engine
    app.state.session_factory = create_session_factory(engine)
    app.state.redis = create_redis_client(str(settings.redis_url))

    yield

    await app.state.db_engine.dispose()
    await app.state.redis.aclose()


def create_app() -> FastAPI:
    app = FastAPI(title="ledger-core", version="0.1.0", lifespan=lifespan)
    app.include_router(health_router)
    app.include_router(owners_router)
    app.include_router(accounts_router)
    return app


app = create_app()
