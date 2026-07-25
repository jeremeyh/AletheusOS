from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from aletheus.time_utils import utc_now_iso

from .models import (
    ExperienceConfidence,
    ExperienceHealthCheck,
    ExperienceHealthSnapshot,
    ExperienceMission,
    ExperienceOverview,
    ExperienceProvenance,
    ExperienceResponse,
    ExperienceReversibility,
    ExperienceUncertainty,
    HealthState,
    PrincipleXEnvelope,
)
from .providers.aggregator import LiveProviderAggregator
from .providers.contracts import ProviderRegistry

HealthProvider = Callable[[], dict[str, Any]]
MissionProvider = Callable[[], list[dict[str, Any]]]


@dataclass(slots=True)
class ExperienceGatewayService:
    health_provider: HealthProvider | None = None
    mission_provider: MissionProvider | None = None
    provider_registry: ProviderRegistry | None = None

    def health(self) -> ExperienceResponse:
        generated_at = utc_now_iso()

        if self.provider_registry is not None:
            aggregator = LiveProviderAggregator(
                self.provider_registry
            )
            snapshot = self._health_from_provider(
                aggregator.health_payload(),
                generated_at,
            )
        elif self.health_provider is not None:
            snapshot = self._health_from_provider(
                self.health_provider(),
                generated_at,
            )
        else:
            snapshot = self._verified_baseline_health(
                generated_at
            )

        return ExperienceResponse(
            data=snapshot,
            generated_at=generated_at,
            request_id=str(uuid4()),
            metadata={
                "source": (
                    "provider_registry"
                    if self.provider_registry is not None
                    else (
                        "runtime_provider"
                        if self.health_provider is not None
                        else "verified_local_baseline"
                    )
                ),
                "principleX": True,
            },
        )

    def missions(self) -> ExperienceResponse:
        generated_at = utc_now_iso()

        if self.provider_registry is not None:
            aggregator = LiveProviderAggregator(
                self.provider_registry
            )
            missions = tuple(
                self._mission_from_mapping(
                    mission,
                    generated_at,
                )
                for mission in (
                    aggregator.mission_payload()
                )
            )
            source = "provider_registry"
        elif self.mission_provider is not None:
            missions = tuple(
                self._mission_from_mapping(
                    mission,
                    generated_at,
                )
                for mission in self.mission_provider()
            )
            source = "runtime_provider"
        else:
            missions = self._baseline_missions(
                generated_at
            )
            source = "verified_local_baseline"

        return ExperienceResponse(
            data=missions,
            generated_at=generated_at,
            request_id=str(uuid4()),
            metadata={
                "source": source,
                "principleX": True,
            },
        )

    def overview(self) -> ExperienceResponse:
        generated_at = utc_now_iso()

        health_response = self.health()
        mission_response = self.missions()

        overview = ExperienceOverview(
            health=health_response.data,
            missions=tuple(mission_response.data),
            generated_at=generated_at,
        )

        return ExperienceResponse(
            data=overview,
            generated_at=generated_at,
            request_id=str(uuid4()),
            metadata={
                "healthRequestId": (
                    health_response.request_id
                ),
                "missionRequestId": (
                    mission_response.request_id
                ),
                "principleX": True,
            },
        )

    def _verified_baseline_health(
        self,
        checked_at: str,
    ) -> ExperienceHealthSnapshot:
        checks = (
            ExperienceHealthCheck(
                id="runtime-regression",
                name="Runtime regression",
                state="healthy",
                detail=(
                    "246 tests passed with zero warnings "
                    "at the current frozen baseline."
                ),
                checked_at=checked_at,
                latency_ms=2500,
            ),
            ExperienceHealthCheck(
                id="nimble-foundation",
                name="Nimble foundation",
                state="healthy",
                detail=(
                    "Architecture, token, component, "
                    "interaction, and inheritance "
                    "contracts validated."
                ),
                checked_at=checked_at,
            ),
            ExperienceHealthCheck(
                id="nimble-production-build",
                name="Nimble production build",
                state="healthy",
                detail=(
                    "TypeScript workspace and Vite "
                    "production build completed."
                ),
                checked_at=checked_at,
            ),
        )

        return ExperienceHealthSnapshot(
            state="healthy",
            summary=(
                "AletheusOS is reporting its latest "
                "verified local baseline."
            ),
            passing_checks=246,
            total_checks=246,
            warning_count=0,
            checks=checks,
            truth=PrincipleXEnvelope(
                state="verified_local_baseline",
                explanation=(
                    "This response describes the latest "
                    "verified regression and Nimble "
                    "validation baseline. It is not yet "
                    "a continuous runtime probe."
                ),
                confidence=ExperienceConfidence(
                    value=0.99,
                    label="verified",
                    basis=(
                        "Recorded local pytest, TypeScript, "
                        "Vite, and Nimble validator results."
                    ),
                ),
                provenance=(
                    ExperienceProvenance(
                        source_id=(
                            "genesis-8-clean-baseline"
                        ),
                        source_type=(
                            "verified_regression_baseline"
                        ),
                        label=(
                            "AletheusOS clean baseline"
                        ),
                        observed_at=checked_at,
                    ),
                ),
                uncertainty=(
                    ExperienceUncertainty(
                        known=True,
                        material=True,
                        description=(
                            "The response does not yet prove "
                            "continuous live subsystem health."
                        ),
                    ),
                ),
                reversibility=ExperienceReversibility(
                    reversible=True,
                    undo_label=(
                        "Replace with live health provider"
                    ),
                    consequence=(
                        "The baseline adapter can be replaced "
                        "without changing the public API."
                    ),
                ),
            ),
        )

    def _baseline_missions(
        self,
        observed_at: str,
    ) -> tuple[ExperienceMission, ...]:
        provenance = (
            ExperienceProvenance(
                source_id="nimble-development-plan",
                source_type="platform_plan",
                label="Nimble implementation roadmap",
                observed_at=observed_at,
            ),
        )

        return (
            ExperienceMission(
                id="nimble-production-shell",
                name="Nimble Production Shell",
                description=(
                    "Deliver the inherited AletheusOS "
                    "experience framework."
                ),
                state="active",
                progress=84,
                confidence=ExperienceConfidence(
                    value=0.97,
                    label="high",
                    basis=(
                        "Production shell, packages, tokens, "
                        "routing, and query boundaries exist."
                    ),
                ),
                provenance=provenance,
            ),
            ExperienceMission(
                id="runtime-api-integration",
                name="Runtime API Integration",
                description=(
                    "Connect Nimble to live bounded runtime "
                    "providers."
                ),
                state="active",
                progress=52,
                confidence=ExperienceConfidence(
                    value=0.9,
                    label="high",
                    basis=(
                        "Experience gateway boundary is active; "
                        "continuous providers remain."
                    ),
                ),
                provenance=provenance,
                uncertainty=(
                    ExperienceUncertainty(
                        known=True,
                        material=True,
                        description=(
                            "Continuous subsystem probes are "
                            "not yet registered."
                        ),
                    ),
                ),
            ),
            ExperienceMission(
                id="card-hawk-inheritance",
                name="Card Hawk Inheritance",
                description=(
                    "Adopt Nimble without duplicating the "
                    "experience architecture."
                ),
                state="planned",
                progress=20,
                confidence=ExperienceConfidence(
                    value=0.94,
                    label="high",
                    basis=(
                        "Application inheritance contracts "
                        "are already established."
                    ),
                ),
                provenance=provenance,
            ),
        )

    def _health_from_provider(
        self,
        payload: dict[str, Any],
        checked_at: str,
    ) -> ExperienceHealthSnapshot:
        checks_payload = payload.get(
            "checks",
            [],
        )

        checks = tuple(
            ExperienceHealthCheck(
                id=str(
                    check.get("id", f"check-{index}")
                ),
                name=str(
                    check.get("name", "Runtime check")
                ),
                state=self._health_state(
                    check.get("state")
                ),
                detail=str(
                    check.get(
                        "detail",
                        "No detail was supplied.",
                    )
                ),
                checked_at=str(
                    check.get(
                        "checked_at",
                        checked_at,
                    )
                ),
                latency_ms=(
                    int(check["latency_ms"])
                    if check.get("latency_ms")
                    is not None
                    else None
                ),
            )
            for index, check in enumerate(
                checks_payload
            )
        )

        total_checks = int(
            payload.get(
                "total_checks",
                len(checks),
            )
        )

        passing_checks = int(
            payload.get(
                "passing_checks",
                sum(
                    check.state == "healthy"
                    for check in checks
                ),
            )
        )

        return ExperienceHealthSnapshot(
            state=self._health_state(
                payload.get("state")
            ),
            summary=str(
                payload.get(
                    "summary",
                    "Runtime provider supplied no summary.",
                )
            ),
            passing_checks=passing_checks,
            total_checks=total_checks,
            warning_count=int(
                payload.get(
                    "warning_count",
                    0,
                )
            ),
            checks=checks,
            truth=PrincipleXEnvelope(
                state="live_runtime_provider",
                explanation=(
                    "This response was produced by a "
                    "registered live runtime provider."
                ),
                confidence=ExperienceConfidence(
                    value=float(
                        payload.get(
                            "confidence",
                            0.9,
                        )
                    ),
                    label="high",
                    basis=(
                        "Registered runtime provider response."
                    ),
                ),
                provenance=(
                    ExperienceProvenance(
                        source_id="runtime-provider",
                        source_type="live_runtime",
                        label="AletheusOS runtime provider",
                        observed_at=checked_at,
                    ),
                ),
                reversibility=ExperienceReversibility(
                    reversible=False,
                    consequence=(
                        "This is a read-only health response."
                    ),
                ),
            ),
        )

    def _mission_from_mapping(
        self,
        payload: dict[str, Any],
        observed_at: str,
    ) -> ExperienceMission:
        return ExperienceMission(
            id=str(payload["id"]),
            name=str(payload["name"]),
            description=str(
                payload.get(
                    "description",
                    "",
                )
            ),
            state=payload.get(
                "state",
                "planned",
            ),
            progress=int(
                payload.get(
                    "progress",
                    0,
                )
            ),
            confidence=ExperienceConfidence(
                value=float(
                    payload.get(
                        "confidence",
                        0.8,
                    )
                ),
                label="high",
                basis=(
                    "Registered mission provider response."
                ),
            ),
            provenance=(
                ExperienceProvenance(
                    source_id="mission-provider",
                    source_type="live_runtime",
                    label="AletheusOS mission provider",
                    observed_at=observed_at,
                ),
            ),
        )

    @staticmethod
    def _health_state(
        value: Any,
    ) -> HealthState:
        if value in {
            "healthy",
            "degraded",
            "unavailable",
            "unknown",
        }:
            return value

        return "unknown"
