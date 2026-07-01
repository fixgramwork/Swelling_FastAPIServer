from fastapi.testclient import TestClient

from services.gateway.app.main import app as gateway_app
from services.swelling.app.main import app as swelling_app


def test_swelling_report_routes_are_removed() -> None:
    client = TestClient(swelling_app)

    assert client.get("/reports").status_code == 404
    assert client.post("/reports", json={}).status_code == 404
    assert client.get("/reports/report-id").status_code == 404
    assert client.get("/users/user-id/reports").status_code == 404


def test_gateway_does_not_expose_swelling_proxy_route() -> None:
    paths = {route.path for route in gateway_app.routes}

    assert "/api/v1/swelling/{path:path}" not in paths
