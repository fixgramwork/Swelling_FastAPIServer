from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel, Field

from swelling_common.health import health_payload


app = FastAPI(title="Notifications Service", version="0.1.0")


class NotificationCreate(BaseModel):
    user_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=120)
    message: str = Field(..., min_length=1, max_length=500)


class Notification(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    created_at: datetime
    sent: bool


notifications: dict[str, Notification] = {}


@app.get("/health", tags=["health"])
async def health() -> dict[str, object]:
    return health_payload("notifications")


@app.post(
    "/notifications",
    response_model=Notification,
    status_code=status.HTTP_201_CREATED,
    tags=["notifications"],
)
async def create_notification(payload: NotificationCreate) -> Notification:
    notification = Notification(
        id=str(uuid4()),
        user_id=payload.user_id,
        title=payload.title,
        message=payload.message,
        created_at=datetime.now(UTC),
        sent=True,
    )
    notifications[notification.id] = notification
    return notification


@app.get("/notifications", response_model=list[Notification], tags=["notifications"])
async def list_notifications() -> list[Notification]:
    return list(notifications.values())
