"""Adapters that connect existing AletheusOS institutions safely."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .events import CivilizationEvent
from .readiness import (
    ReadinessCheck,
    ReadinessState,
)

EventSink = Callable[[CivilizationEvent], Any]


def _as_mapping(value: Any) -> dict[str, Any]:
    if value is None:
        return {}

    if isinstance(value, dict):
        return value

    if hasattr(value, "to_dict"):
        converted = value.to_dict()
        return converted if isinstance(converted, dict) else {
            "value": converted,
        }

    return {"value": value}


@dataclass(slots=True)
class InstitutionWiring:
    """
    Safe adapters for existing institutional implementations.

    Services remain optional. Missing services produce explicit degraded
    checks instead of false operational claims.
    """

    root: Path
    watch_tower: Any | None = None
    spa: Any | None = None
    homeostasis: Any | None = None
    council: Any | None = None
    ledger: Any | None = None
    event_sink: EventSink | None = None

    def publish(
        self,
        event_type: str,
        source: str,
        payload: dict[str, Any] | None = None,
    ) -> CivilizationEvent:
        event = CivilizationEvent.create(
            event_type=event_type,
            source=source,
            payload=payload,
        )

        if self.event_sink is not None:
            self.event_sink(event)

        return event

    def run_watch_tower(self) -> ReadinessCheck:
        if self.watch_tower is None:
            return ReadinessCheck(
                name="watch_tower_activation",
                institution_id="aletheus.watch_tower",
                state=ReadinessState.DEGRADED,
                message="Watch Tower implementation was not supplied.",
            )

        try:
            if hasattr(self.watch_tower, "scan"):
                result = self.watch_tower.scan()
            elif hasattr(self.watch_tower, "verify"):
                result = self.watch_tower.verify()
            elif hasattr(self.watch_tower, "evaluate"):
                result = self.watch_tower.evaluate()
            else:
                return ReadinessCheck(
                    name="watch_tower_activation",
                    institution_id="aletheus.watch_tower",
                    state=ReadinessState.DEGRADED,
                    message=(
                        "Watch Tower exists but exposes no compatible "
                        "scan, verify, or evaluate method."
                    ),
                )

            evidence = _as_mapping(result)
            self.publish(
                "WatchTowerAssessmentCompleted",
                "aletheus.watch_tower",
                evidence,
            )

            return ReadinessCheck(
                name="watch_tower_activation",
                institution_id="aletheus.watch_tower",
                state=ReadinessState.READY,
                message="Watch Tower completed an institutional assessment.",
                evidence=evidence,
            )
        except Exception as exc:
            return ReadinessCheck(
                name="watch_tower_activation",
                institution_id="aletheus.watch_tower",
                state=ReadinessState.FAILED,
                message=str(exc),
            )

    def run_spa(self) -> ReadinessCheck:
        if self.spa is None:
            return ReadinessCheck(
                name="spa_assessment",
                institution_id="aletheus.spa",
                state=ReadinessState.DEGRADED,
                message="Spectrum Platform Analyzer was not supplied.",
            )

        try:
            if hasattr(self.spa, "assess"):
                result = self.spa.assess(str(self.root))
            elif hasattr(self.spa, "analyze"):
                try:
                    result = self.spa.analyze(str(self.root))
                except TypeError:
                    result = self.spa.analyze()
            elif hasattr(self.spa, "initialize"):
                result = self.spa.initialize()
            elif hasattr(self.spa, "health"):
                result = self.spa.health()
            else:
                return ReadinessCheck(
                    name="spa_assessment",
                    institution_id="aletheus.spa",
                    state=ReadinessState.DEGRADED,
                    message=(
                        "SPA exists but exposes no compatible assessment "
                        "or health method."
                    ),
                )

            evidence = _as_mapping(result)
            self.publish(
                "PlatformAssessmentCompleted",
                "aletheus.spa",
                evidence,
            )

            return ReadinessCheck(
                name="spa_assessment",
                institution_id="aletheus.spa",
                state=ReadinessState.READY,
                message="SPA produced a platform assessment.",
                evidence=evidence,
            )
        except Exception as exc:
            return ReadinessCheck(
                name="spa_assessment",
                institution_id="aletheus.spa",
                state=ReadinessState.FAILED,
                message=str(exc),
            )

    def update_homeostasis(
        self,
        checks: list[ReadinessCheck],
    ) -> ReadinessCheck:
        if self.homeostasis is None:
            return ReadinessCheck(
                name="homeostasis_equilibrium",
                institution_id="aletheus.homeostasis",
                state=ReadinessState.DEGRADED,
                message="Homeostasis implementation was not supplied.",
            )

        try:
            compatible = hasattr(self.homeostasis, "record")
            if not compatible:
                return ReadinessCheck(
                    name="homeostasis_equilibrium",
                    institution_id="aletheus.homeostasis",
                    state=ReadinessState.DEGRADED,
                    message=(
                        "Homeostasis exists but exposes no compatible "
                        "record method."
                    ),
                )

            for check in checks:
                score = {
                    ReadinessState.READY: 100.0,
                    ReadinessState.DEGRADED: 55.0,
                    ReadinessState.SKIPPED: 25.0,
                    ReadinessState.FAILED: 0.0,
                }[check.state]

                self.homeostasis.record(
                    check.institution_id,
                    score,
                    check.message,
                )

            evidence = (
                _as_mapping(self.homeostasis.health())
                if hasattr(self.homeostasis, "health")
                else {"signals_recorded": len(checks)}
            )

            self.publish(
                "HomeostasisUpdated",
                "aletheus.homeostasis",
                evidence,
            )

            state = (
                ReadinessState.READY
                if all(check.state != ReadinessState.FAILED for check in checks)
                else ReadinessState.DEGRADED
            )

            return ReadinessCheck(
                name="homeostasis_equilibrium",
                institution_id="aletheus.homeostasis",
                state=state,
                message="Homeostasis received institutional health signals.",
                evidence=evidence,
            )
        except Exception as exc:
            return ReadinessCheck(
                name="homeostasis_equilibrium",
                institution_id="aletheus.homeostasis",
                state=ReadinessState.FAILED,
                message=str(exc),
            )

    def escalate_to_council(
        self,
        checks: list[ReadinessCheck],
    ) -> ReadinessCheck:
        actionable = [
            check
            for check in checks
            if check.state in {
                ReadinessState.DEGRADED,
                ReadinessState.FAILED,
            }
        ]

        if not actionable:
            return ReadinessCheck(
                name="council_escalation",
                institution_id="aletheus.council",
                state=ReadinessState.SKIPPED,
                message="No institutional findings required escalation.",
            )

        if self.council is None:
            return ReadinessCheck(
                name="council_escalation",
                institution_id="aletheus.council",
                state=ReadinessState.DEGRADED,
                message=(
                    f"{len(actionable)} finding(s) require governance, "
                    "but no Council implementation was supplied."
                ),
                evidence={
                    "actionable_findings": [
                        check.to_dict()
                        for check in actionable
                    ],
                },
            )

        proposal = {
            "proposal": "Civilization bootstrap remediation",
            "findings": [
                check.to_dict()
                for check in actionable
            ],
        }

        try:
            if hasattr(self.council, "deliberate"):
                result = self.council.deliberate(proposal)
            elif hasattr(self.council, "evaluate"):
                result = self.council.evaluate(proposal)
            elif hasattr(self.council, "process"):
                result = self.council.process(proposal)
            else:
                return ReadinessCheck(
                    name="council_escalation",
                    institution_id="aletheus.council",
                    state=ReadinessState.DEGRADED,
                    message=(
                        "Council exists but exposes no compatible "
                        "deliberate, evaluate, or process method."
                    ),
                    evidence=proposal,
                )

            evidence = _as_mapping(result)
            self.publish(
                "CouncilDeliberationCompleted",
                "aletheus.council",
                evidence,
            )

            return ReadinessCheck(
                name="council_escalation",
                institution_id="aletheus.council",
                state=ReadinessState.READY,
                message=(
                    f"Council processed {len(actionable)} escalated "
                    "institutional finding(s)."
                ),
                evidence=evidence,
            )
        except Exception as exc:
            return ReadinessCheck(
                name="council_escalation",
                institution_id="aletheus.council",
                state=ReadinessState.FAILED,
                message=str(exc),
                evidence=proposal,
            )

    def record_boot(
        self,
        payload: dict[str, Any],
    ) -> ReadinessCheck:
        event = self.publish(
            "CivilizationBootstrapCompleted",
            "aletheus.institutional_civilization",
            payload,
        )

        if self.ledger is None:
            return ReadinessCheck(
                name="ledger_boot_record",
                institution_id="aletheus.ledger",
                state=ReadinessState.DEGRADED,
                message=(
                    "Bootstrap event was emitted, but no Ledger adapter "
                    "was supplied."
                ),
                evidence=event.to_dict(),
            )

        try:
            if hasattr(self.ledger, "record_event"):
                result = self.ledger.record_event(event.to_dict())
            elif hasattr(self.ledger, "append"):
                result = self.ledger.append(event.to_dict())
            else:
                return ReadinessCheck(
                    name="ledger_boot_record",
                    institution_id="aletheus.ledger",
                    state=ReadinessState.DEGRADED,
                    message=(
                        "Ledger exists but its current decision-record API "
                        "does not yet expose a generic institutional-event "
                        "adapter."
                    ),
                    evidence=event.to_dict(),
                )

            return ReadinessCheck(
                name="ledger_boot_record",
                institution_id="aletheus.ledger",
                state=ReadinessState.READY,
                message="Civilization bootstrap was recorded in Ledger.",
                evidence=_as_mapping(result),
            )
        except Exception as exc:
            return ReadinessCheck(
                name="ledger_boot_record",
                institution_id="aletheus.ledger",
                state=ReadinessState.FAILED,
                message=str(exc),
                evidence=event.to_dict(),
            )
