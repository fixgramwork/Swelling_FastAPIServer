from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from swelling_common.health import health_payload


app = FastAPI(title="Users Service", version="0.1.0")


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    email: EmailStr


class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime


users: dict[str, User] = {}


@app.get("/health", tags=["health"])
async def health() -> dict[str, object]:
    return health_payload("users")


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["users"])
async def create_user(payload: UserCreate) -> User:
    user = User(
        id=str(uuid4()),
        name=payload.name,
        email=payload.email,
        created_at=datetime.now(UTC),
    )
    users[user.id] = user
    return user


@app.get("/users", response_model=list[User], tags=["users"])
async def list_users() -> list[User]:
    return list(users.values())


@app.get("/users/{user_id}", response_model=User, tags=["users"])
async def get_user(user_id: str) -> User:
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
