from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def health_payload(service: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "service": service,
        "status": "ok",
        "timestamp": datetime.now(UTC).isoformat(),
    }
    if extra:
        payload.update(extra)
    return payload
