from __future__ import annotations

from fastapi.testclient import TestClient

from aletheus.experience_gateway.fastapi_app import (
    create_app,
)


def test_health_endpoint_matches_nimble_contract() -> None:
    client = TestClient(create_app())

    response = client.get("/api/runtime/health")

    assert response.status_code == 200

    payload = response.json()

    assert payload["state"] == "healthy"
    assert payload["passingChecks"] == 246
    assert payload["truth"]["state"] == (
        "verified_local_baseline"
    )


def test_missions_endpoint_returns_array() -> None:
    client = TestClient(create_app())

    response = client.get("/api/missions")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()


def test_overview_endpoint_returns_combined_state() -> None:
    client = TestClient(create_app())

    response = client.get("/api/runtime/overview")

    assert response.status_code == 200

    payload = response.json()

    assert "health" in payload
    assert "missions" in payload


def test_provider_registry_endpoint_discloses_sources() -> None:
    client = TestClient(create_app())

    response = client.get(
        "/api/experience/providers"
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["mode"] in {
        "provider_registry",
        "legacy_provider",
    }
