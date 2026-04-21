from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live", summary="Liveliness Check", description="Check if the service is alive and responsive.")
async def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})

@router.get("/ready", summary="Readiness Check", description="Check if the service is ready to handle requests.")
async def readiness_check(request: Request) -> JSONResponse:
    checks: dict[str, str] = {}
    ok = True

    # Database check
    try:
        async with request.app.state.db_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception: # noqa: BLE001
        checks["database"] = "unavailable"
        ok = False

    # Redis check
    try:
        await request.app.state.redis.ping()
        checks["redis"] = "ok"
    except Exception: # noqa: BLE001
        checks["redis"] = "unavailable"
        ok = False

    status_code = 200 if ok else 503
    return JSONResponse(
        status_code=status_code,
        content={"status": "ok" if ok else "degraded", "checks": checks},
    )