from __future__ import annotations

from fastapi import FastAPI

from swelling_common.health import health_payload


app = FastAPI(title="Swelling Service", version="0.1.0")


@app.get("/health", tags=["health"])
async def health() -> dict[str, object]:
    return health_payload("swelling")
