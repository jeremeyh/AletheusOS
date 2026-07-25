"""Immutable Constitutional Runtime Observatory models."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any
from uuid import UUID, uuid4


class ObservatoryHealthBand(StrEnum):
    """Canonical aggregate-health bands."""

    EXCELLENT = "excellent"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"


class ObservatoryDriftKind(StrEnum):
    """Canonical drift classifications."""

    SERVICE_INVENTORY = "service_inventory"
    SERVICE_STATE = "service_state"
    SERVICE_HEALTH = "service_health"
    POLICY_REGISTRY = "policy_registry"
    DEPENDENCY_TOPOLOGY = "dependency_topology"
    GOVERNANCE_STATE = "governance_state"


@dataclass(frozen=True, slots=True)
class ObservatorySubsystemScore:
    """One immutable subsystem score."""

    subsystem: str
    score: float
    band: ObservatoryHealthBand
    reason: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 100.0:
            raise ValueError(
                "score must be between 0 and 100."
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "subsystem": self.subsystem,
            "score": self.score,
            "band": self.band.value,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class ConstitutionalRuntimeHealthScore:
    """Aggregate constitutional runtime score."""

    generated_at: datetime
    overall_score: float
    band: ObservatoryHealthBand
    subsystems: tuple[
        ObservatorySubsystemScore,
        ...,
    ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": (
                self.generated_at.isoformat()
            ),
            "overall_score": self.overall_score,
            "band": self.band.value,
            "subsystems": [
                item.to_dict()
                for item in self.subsystems
            ],
        }


@dataclass(frozen=True, slots=True)
class ObservatoryDrift:
    """One immutable drift observation."""

    kind: ObservatoryDriftKind
    subject: str
    baseline: Any
    observed: Any
    severity: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "subject": self.subject,
            "baseline": self.baseline,
            "observed": self.observed,
            "severity": self.severity,
            "explanation": self.explanation,
        }


@dataclass(frozen=True, slots=True)
class ObservatorySnapshot:
    """Immutable constitutional control-plane snapshot."""

    snapshot_id: UUID
    generated_at: datetime
    sequence: int
    kernel: Mapping[str, Any]
    supervisor: Mapping[str, Any]
    executive: Mapping[str, Any]
    policy_engine: Mapping[str, Any]
    governor: Mapping[str, Any]
    council: Mapping[str, Any]
    dependency_manager: Mapping[str, Any]
    services: tuple[Mapping[str, Any], ...]
    health: ConstitutionalRuntimeHealthScore
    drift: tuple[ObservatoryDrift, ...]

    @classmethod
    def create(
        cls,
        *,
        sequence: int,
        kernel: Mapping[str, Any],
        supervisor: Mapping[str, Any],
        executive: Mapping[str, Any],
        policy_engine: Mapping[str, Any],
        governor: Mapping[str, Any],
        council: Mapping[str, Any],
        dependency_manager: Mapping[str, Any],
        services: tuple[
            Mapping[str, Any],
            ...,
        ],
        health: ConstitutionalRuntimeHealthScore,
        drift: tuple[ObservatoryDrift, ...],
    ) -> ObservatorySnapshot:
        return cls(
            snapshot_id=uuid4(),
            generated_at=datetime.now(UTC),
            sequence=sequence,
            kernel=MappingProxyType(dict(kernel)),
            supervisor=MappingProxyType(
                dict(supervisor)
            ),
            executive=MappingProxyType(
                dict(executive)
            ),
            policy_engine=MappingProxyType(
                dict(policy_engine)
            ),
            governor=MappingProxyType(
                dict(governor)
            ),
            council=MappingProxyType(
                dict(council)
            ),
            dependency_manager=MappingProxyType(
                dict(dependency_manager)
            ),
            services=tuple(
                MappingProxyType(dict(service))
                for service in services
            ),
            health=health,
            drift=drift,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": str(
                self.snapshot_id
            ),
            "generated_at": (
                self.generated_at.isoformat()
            ),
            "sequence": self.sequence,
            "kernel": dict(self.kernel),
            "supervisor": dict(self.supervisor),
            "executive": dict(self.executive),
            "policy_engine": dict(
                self.policy_engine
            ),
            "governor": dict(self.governor),
            "council": dict(self.council),
            "dependency_manager": dict(
                self.dependency_manager
            ),
            "services": [
                dict(service)
                for service in self.services
            ],
            "health": self.health.to_dict(),
            "drift": [
                item.to_dict()
                for item in self.drift
            ],
        }


@dataclass(frozen=True, slots=True)
class ObservatoryTimelineEntry:
    """Immutable constitutional timeline entry."""

    sequence: int
    recorded_at: datetime
    event_type: str
    subject: str
    summary: str
    snapshot_id: UUID

    def to_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "recorded_at": (
                self.recorded_at.isoformat()
            ),
            "event_type": self.event_type,
            "subject": self.subject,
            "summary": self.summary,
            "snapshot_id": str(
                self.snapshot_id
            ),
        }


@dataclass(frozen=True, slots=True)
class ObservatoryExplanation:
    """Immutable explainability response."""

    subject: str
    generated_at: datetime
    explanation: str
    evidence: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject": self.subject,
            "generated_at": (
                self.generated_at.isoformat()
            ),
            "explanation": self.explanation,
            "evidence": list(self.evidence),
        }


@dataclass(frozen=True, slots=True)
class ObservatoryStatistics:
    """Immutable CRO statistics."""

    snapshots: int
    timeline_entries: int
    drift_observations: int
    explanations: int
    latest_health_score: float | None

    def to_dict(
        self,
    ) -> dict[str, int | float | None]:
        return {
            "snapshots": self.snapshots,
            "timeline_entries": (
                self.timeline_entries
            ),
            "drift_observations": (
                self.drift_observations
            ),
            "explanations": self.explanations,
            "latest_health_score": (
                self.latest_health_score
            ),
        }
