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

    assert payload["state"] in {
        "healthy",
        "degraded",
        "unavailable",
        "unknown",
    }

    assert payload["totalChecks"] == 4
    assert 0 <= payload["passingChecks"] <= 4
    assert payload["warningCount"] >= 0

    assert payload["truth"]["state"] == ("live_runtime_provider")

    check_ids = {check["id"] for check in payload["checks"]}

    assert check_ids == {
        "repository-structure",
        "runtime-import",
        "experience-gateway-import",
        "nimble-production-build",
    }


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

    response = client.get("/api/experience/providers")

    assert response.status_code == 200

    payload = response.json()

    assert payload["mode"] in {
        "provider_registry",
        "legacy_provider",
    }


def test_command_preview_and_execution_flow() -> None:
    client = TestClient(create_app())

    preview_response = client.post(
        "/api/commands/preview",
        json={
            "command_id": "runtime.describe",
            "arguments": {},
        },
    )

    assert preview_response.status_code == 200

    preview = preview_response.json()

    execution_response = client.post(
        "/api/commands/execute",
        json={
            "preview_id": preview["preview_id"],
            "authorization_id": None,
            "idempotency_key": "test-command-flow",
        },
    )

    assert execution_response.status_code == 200

    execution = execution_response.json()

    assert execution["state"] == "executed"
    assert execution["result"]["mutated"] is False


def test_mutating_command_requires_authorization() -> None:
    client = TestClient(create_app())

    preview_response = client.post(
        "/api/commands/preview",
        json={
            "command_id": ("experience.inspector.set"),
            "arguments": {
                "open": False,
            },
        },
    )

    preview = preview_response.json()

    execution_response = client.post(
        "/api/commands/execute",
        json={
            "preview_id": preview["preview_id"],
            "authorization_id": None,
        },
    )

    assert execution_response.status_code == 403
