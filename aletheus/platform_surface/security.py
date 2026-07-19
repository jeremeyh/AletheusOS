"""Public Security Civilization Surface."""

from __future__ import annotations

from typing import Any


class SecuritySurface:
    """
    Stable application-facing Security Civilization API.

    Applications do not need to know how Cases, Missions, TIME™, institutional
    executors, events, or the Ledger are composed internally.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        orchestrator,
    ) -> None:
        self._orchestrator = orchestrator

    def respond_to_integrity_finding(
        self,
        *,
        entity_id: str,
        severity: str,
        finding: dict[str, Any],
    ):
        return (
            self._orchestrator
            .respond_to_integrity_finding(
                entity_id=entity_id,
                severity=severity,
                finding=finding,
            )
        )

    def case(
        self,
        case_id: str,
    ):
        return (
            self._orchestrator
            .case_engine
            .registry
            .require(case_id)
        )

    def mission(
        self,
        mission_id: str,
    ):
        return (
            self._orchestrator
            .mission_engine
            .registry
            .require(mission_id)
        )

    def history(
        self,
        correlation_id: str,
    ):
        return self._orchestrator.history(
            correlation_id
        )

    def provenance(
        self,
        event_id: str,
    ):
        return self._orchestrator.provenance(
            event_id
        )

    def health(self) -> dict[str, Any]:
        orchestrator_health = (
            self._orchestrator.health()
        )

        return {
            "name": (
                "AletheusOS Security Surface™"
            ),
            "version": self.VERSION,
            "status": (
                orchestrator_health.get(
                    "status",
                    "unknown",
                )
            ),
            "responses": (
                orchestrator_health.get(
                    "responses",
                    0,
                )
            ),
            "failures": (
                orchestrator_health.get(
                    "failures",
                    0,
                )
            ),
        }
