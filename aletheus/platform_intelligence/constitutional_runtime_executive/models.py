"""Immutable Constitutional Runtime Executive models."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any
from uuid import UUID, uuid4


class ExecutiveDecision(StrEnum):
    """Canonical CRX decisions."""

    NO_ACTION = "no_action"
    OBSERVE = "observe"
    RESTART_SERVICE = "restart_service"
    RESTART_DEPENDENCY_CHAIN = (
        "restart_dependency_chain"
    )
    PAUSE_SERVICE = "pause_service"
    STOP_RUNTIME = "stop_runtime"
    ESCALATE = "escalate"
    REQUIRE_MANUAL_ACTION = (
        "require_manual_action"
    )


class ExecutiveRisk(StrEnum):
    """Canonical executive risk levels."""

    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class ExecutiveContext:
    """Immutable runtime context consumed by CRX."""

    generated_at: datetime
    runtime_state: str
    kernel_state: str
    service_count: int
    healthy: int
    warning: int
    degraded: int
    critical: int
    offline: int
    unknown: int
    recoverable_services: tuple[str, ...]
    restart_attempts: Mapping[str, int]

    def __post_init__(self) -> None:
        if self.generated_at.tzinfo is None:
            raise ValueError(
                "generated_at must include timezone."
            )

        object.__setattr__(
            self,
            "generated_at",
            self.generated_at.astimezone(UTC),
        )
        object.__setattr__(
            self,
            "recoverable_services",
            tuple(sorted(self.recoverable_services)),
        )
        object.__setattr__(
            self,
            "restart_attempts",
            MappingProxyType(
                dict(self.restart_attempts)
            ),
        )

    @classmethod
    def create(
        cls,
        *,
        runtime_state: str,
        kernel_state: str,
        service_count: int,
        healthy: int,
        warning: int,
        degraded: int,
        critical: int,
        offline: int,
        unknown: int,
        recoverable_services: tuple[str, ...],
        restart_attempts: Mapping[str, int],
    ) -> ExecutiveContext:
        return cls(
            generated_at=datetime.now(UTC),
            runtime_state=runtime_state,
            kernel_state=kernel_state,
            service_count=service_count,
            healthy=healthy,
            warning=warning,
            degraded=degraded,
            critical=critical,
            offline=offline,
            unknown=unknown,
            recoverable_services=(
                recoverable_services
            ),
            restart_attempts=restart_attempts,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": (
                self.generated_at.isoformat()
            ),
            "runtime_state": self.runtime_state,
            "kernel_state": self.kernel_state,
            "service_count": self.service_count,
            "healthy": self.healthy,
            "warning": self.warning,
            "degraded": self.degraded,
            "critical": self.critical,
            "offline": self.offline,
            "unknown": self.unknown,
            "recoverable_services": list(
                self.recoverable_services
            ),
            "restart_attempts": dict(
                self.restart_attempts
            ),
        }


@dataclass(frozen=True, slots=True)
class ExecutivePolicyResult:
    """One immutable policy evaluation result."""

    policy_id: str
    matched: bool
    decision: ExecutiveDecision
    risk: ExecutiveRisk
    confidence: float
    reason: str
    affected_services: tuple[str, ...]

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "confidence must be between 0 and 1."
            )

        object.__setattr__(
            self,
            "affected_services",
            tuple(sorted(self.affected_services)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "matched": self.matched,
            "decision": self.decision.value,
            "risk": self.risk.value,
            "confidence": self.confidence,
            "reason": self.reason,
            "affected_services": list(
                self.affected_services
            ),
        }


@dataclass(frozen=True, slots=True)
class ExecutiveRecommendation:
    """Auditable executive recommendation."""

    recommendation_id: UUID
    generated_at: datetime
    decision: ExecutiveDecision
    risk: ExecutiveRisk
    confidence: float
    reason: str
    affected_services: tuple[str, ...]
    policy_results: tuple[
        ExecutivePolicyResult,
        ...,
    ]

    @classmethod
    def create(
        cls,
        *,
        decision: ExecutiveDecision,
        risk: ExecutiveRisk,
        confidence: float,
        reason: str,
        affected_services: tuple[str, ...],
        policy_results: tuple[
            ExecutivePolicyResult,
            ...,
        ],
    ) -> ExecutiveRecommendation:
        return cls(
            recommendation_id=uuid4(),
            generated_at=datetime.now(UTC),
            decision=decision,
            risk=risk,
            confidence=confidence,
            reason=reason,
            affected_services=tuple(
                sorted(affected_services)
            ),
            policy_results=policy_results,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "recommendation_id": str(
                self.recommendation_id
            ),
            "generated_at": (
                self.generated_at.isoformat()
            ),
            "decision": self.decision.value,
            "risk": self.risk.value,
            "confidence": self.confidence,
            "reason": self.reason,
            "affected_services": list(
                self.affected_services
            ),
            "policy_results": [
                result.to_dict()
                for result in self.policy_results
            ],
        }


@dataclass(frozen=True, slots=True)
class ExecutiveRecoveryPlan:
    """Immutable recovery plan derived from a recommendation."""

    plan_id: UUID
    generated_at: datetime
    decision: ExecutiveDecision
    target_services: tuple[str, ...]
    ordered_services: tuple[str, ...]
    requires_manual_approval: bool
    rationale: str

    @classmethod
    def create(
        cls,
        *,
        decision: ExecutiveDecision,
        target_services: tuple[str, ...],
        ordered_services: tuple[str, ...],
        requires_manual_approval: bool,
        rationale: str,
    ) -> ExecutiveRecoveryPlan:
        return cls(
            plan_id=uuid4(),
            generated_at=datetime.now(UTC),
            decision=decision,
            target_services=tuple(
                sorted(target_services)
            ),
            ordered_services=ordered_services,
            requires_manual_approval=(
                requires_manual_approval
            ),
            rationale=rationale,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": str(self.plan_id),
            "generated_at": (
                self.generated_at.isoformat()
            ),
            "decision": self.decision.value,
            "target_services": list(
                self.target_services
            ),
            "ordered_services": list(
                self.ordered_services
            ),
            "requires_manual_approval": (
                self.requires_manual_approval
            ),
            "rationale": self.rationale,
        }


@dataclass(frozen=True, slots=True)
class ExecutiveStatistics:
    """Immutable CRX statistics."""

    evaluations: int
    recommendations: int
    no_action: int
    observe: int
    restart_service: int
    restart_dependency_chain: int
    escalations: int
    manual_actions: int

    def to_dict(self) -> dict[str, int]:
        return {
            "evaluations": self.evaluations,
            "recommendations": self.recommendations,
            "no_action": self.no_action,
            "observe": self.observe,
            "restart_service": (
                self.restart_service
            ),
            "restart_dependency_chain": (
                self.restart_dependency_chain
            ),
            "escalations": self.escalations,
            "manual_actions": (
                self.manual_actions
            ),
        }
