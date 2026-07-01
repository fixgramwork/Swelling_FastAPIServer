from __future__ import annotations

from collections.abc import Awaitable, Callable

import httpx
from fastapi import FastAPI, HTTPException, Request, Response

from swelling_common.health import health_payload
from swelling_common.settings import get_gateway_settings


app = FastAPI(
    title="Swelling API Gateway",
    version="0.1.0",
    description="External entry point for the Swelling MSA backend.",
)


def service_map() -> dict[str, str]:
    settings = get_gateway_settings()
    return {
        "users": settings.users_service_url.rstrip("/"),
        "notifications": settings.notifications_service_url.rstrip("/"),
    }


async def check_downstream(name: str, base_url: str) -> dict[str, str]:
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{base_url}/health")
            response.raise_for_status()
        return {"service": name, "status": "ok"}
    except httpx.HTTPError as exc:
        return {"service": name, "status": "unavailable", "detail": str(exc)}


@app.get("/health", tags=["health"])
async def health() -> dict[str, object]:
    downstream = [
        await check_downstream(name, url)
        for name, url in service_map().items()
    ]
    return health_payload("gateway", {"downstream": downstream})


async def proxy_request(service: str, path: str, request: Request) -> Response:
    services = service_map()
    if service not in services:
        raise HTTPException(status_code=404, detail=f"Unknown service: {service}")

    target_url = f"{services[service]}/{path}".rstrip("/")
    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in {"host", "content-length"}
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            proxied = await client.request(
                method=request.method,
                url=target_url,
                params=request.query_params,
                content=await request.body(),
                headers=headers,
            )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"{service} service is unavailable: {exc}",
        ) from exc

    excluded_headers = {"content-encoding", "transfer-encoding", "connection"}
    response_headers = {
        key: value
        for key, value in proxied.headers.items()
        if key.lower() not in excluded_headers
    }
    return Response(
        content=proxied.content,
        status_code=proxied.status_code,
        headers=response_headers,
        media_type=proxied.headers.get("content-type"),
    )


def gateway_route(service: str) -> Callable[[str, Request], Awaitable[Response]]:
    async def route(path: str, request: Request) -> Response:
        return await proxy_request(service, path, request)

    return route


for service_name in service_map():
    app.add_api_route(
        f"/api/v1/{service_name}/{{path:path}}",
        gateway_route(service_name),
        methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        tags=["gateway"],
    )
