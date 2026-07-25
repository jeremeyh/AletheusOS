from __future__ import annotations

import importlib
import sys

from fastapi.testclient import TestClient

MODULE = "aletheus.experience_gateway.fastapi_app"

OIDC_ENVIRONMENT = {
    "ALETHEUS_OIDC_ISSUER":
        "https://identity.example.test",
    "ALETHEUS_OIDC_AUDIENCE":
        "nimble",
    "ALETHEUS_OIDC_JWKS_URL":
        "https://identity.example.test/.well-known/jwks.json",
}


def load_module(monkeypatch):
    # Remove the previously imported module so app construction
    # occurs exactly once with the current test environment.
    sys.modules.pop(MODULE, None)

    return importlib.import_module(MODULE)


def load_client(
    monkeypatch,
    *,
    auth_mode: str = "local",
    oidc_configured: bool = False,
) -> TestClient:
    monkeypatch.setenv(
        "ALETHEUS_AUTH_MODE",
        auth_mode,
    )

    for name in OIDC_ENVIRONMENT:
        monkeypatch.delenv(
            name,
            raising=False,
        )

    if oidc_configured:
        for name, value in OIDC_ENVIRONMENT.items():
            monkeypatch.setenv(name, value)

    module = load_module(monkeypatch)

    assert module.app is not None

    return TestClient(module.app)


def test_healthz_reports_process_alive(
    monkeypatch,
):
    client = load_client(monkeypatch)

    response = client.get("/healthz")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "alive"
    assert (
        payload["service"]
        == "nimble-experience-gateway"
    )
    assert payload["timestamp"]


def test_readyz_passes_in_local_mode(
    monkeypatch,
):
    client = load_client(
        monkeypatch,
        auth_mode="local",
    )

    response = client.get("/readyz")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "ready"
    assert payload["auth_mode"] == "local"
    assert payload["checks"][
        "auth_mode_supported"
    ] is True


def test_readyz_passes_with_oidc_configuration(
    monkeypatch,
):
    client = load_client(
        monkeypatch,
        auth_mode="oidc",
        oidc_configured=True,
    )

    response = client.get("/readyz")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "ready"
    assert payload["auth_mode"] == "oidc"
    assert payload["checks"][
        "oidc_configuration_present"
    ] is True


def test_readiness_evaluator_reports_missing_oidc_configuration(
    monkeypatch,
):
    monkeypatch.setenv(
        "ALETHEUS_AUTH_MODE",
        "local",
    )

    module = load_module(monkeypatch)

    result = module.evaluate_readiness(
        {
            "ALETHEUS_AUTH_MODE": "oidc",
        }
    )

    assert result["status"] == "not_ready"
    assert result["auth_mode"] == "oidc"
    assert result["checks"][
        "auth_mode_supported"
    ] is True
    assert result["checks"][
        "oidc_configuration_present"
    ] is False


def test_readiness_evaluator_rejects_unknown_auth_mode(
    monkeypatch,
):
    monkeypatch.setenv(
        "ALETHEUS_AUTH_MODE",
        "local",
    )

    module = load_module(monkeypatch)

    result = module.evaluate_readiness(
        {
            "ALETHEUS_AUTH_MODE": "unsupported",
        }
    )

    assert result["status"] == "not_ready"
    assert result["auth_mode"] == "unsupported"
    assert result["checks"][
        "auth_mode_supported"
    ] is False
