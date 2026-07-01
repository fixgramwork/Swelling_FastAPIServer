from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class GatewaySettings:
    users_service_url: str
    swelling_service_url: str
    notifications_service_url: str


@lru_cache
def get_gateway_settings() -> GatewaySettings:
    return GatewaySettings(
        users_service_url=os.getenv("USERS_SERVICE_URL", "http://127.0.0.1:8001"),
        swelling_service_url=os.getenv("SWELLING_SERVICE_URL", "http://127.0.0.1:8002"),
        notifications_service_url=os.getenv(
            "NOTIFICATIONS_SERVICE_URL",
            "http://127.0.0.1:8003",
        ),
    )
