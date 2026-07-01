from fastapi.testclient import TestClient

from services.notifications.app.main import app as notifications_app
from services.swelling.app.main import app as swelling_app
from services.users.app.main import app as users_app


def test_users_health() -> None:
    response = TestClient(users_app).get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "users"


def test_swelling_health() -> None:
    response = TestClient(swelling_app).get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "swelling"


def test_notifications_health() -> None:
    response = TestClient(notifications_app).get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "notifications"
