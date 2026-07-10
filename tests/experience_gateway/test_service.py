from __future__ import annotations

from aletheus.experience_gateway.service import (
    ExperienceGatewayService,
)


def test_health_exposes_verified_baseline_truth() -> None:
    service = ExperienceGatewayService()

    response = service.health()
    payload = response.to_dict()

    assert payload["data"]["state"] == "healthy"
    assert payload["data"]["passingChecks"] == 246
    assert payload["data"]["totalChecks"] == 246
    assert payload["data"]["warningCount"] == 0

    truth = payload["data"]["truth"]

    assert truth["state"] == "verified_local_baseline"
    assert truth["confidence"]["value"] == 0.99
    assert truth["uncertainty"]
    assert truth["provenance"]


def test_missions_expose_bounded_progress() -> None:
    service = ExperienceGatewayService()

    payload = service.missions().to_dict()

    assert payload["data"]

    for mission in payload["data"]:
        assert 0 <= mission["progress"] <= 100


def test_overview_combines_health_and_missions() -> None:
    service = ExperienceGatewayService()

    payload = service.overview().to_dict()

    assert payload["data"]["health"]
    assert payload["data"]["missions"]
    assert payload["data"]["generatedAt"]


def test_registered_health_provider_replaces_baseline() -> None:
    service = ExperienceGatewayService(
        health_provider=lambda: {
            "state": "degraded",
            "summary": "One subsystem is degraded.",
            "total_checks": 2,
            "passing_checks": 1,
            "warning_count": 1,
            "confidence": 0.85,
            "checks": [
                {
                    "id": "one",
                    "name": "Healthy service",
                    "state": "healthy",
                    "detail": "Available",
                },
                {
                    "id": "two",
                    "name": "Degraded service",
                    "state": "degraded",
                    "detail": "High latency",
                },
            ],
        }
    )

    payload = service.health().to_dict()

    assert payload["data"]["state"] == "degraded"
    assert payload["data"]["passingChecks"] == 1
    assert payload["metadata"]["source"] == "runtime_provider"
