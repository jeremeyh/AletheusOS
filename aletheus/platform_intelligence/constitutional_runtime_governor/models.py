"""Immutable models for the Constitutional Runtime Governor."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from types import MappingProxyType
from typing import Any
from uuid import UUID, uuid4

from aletheus.platform_intelligence.constitutional_runtime_executive import (
    ExecutiveDecision,
    ExecutiveRecoveryPlan,
)


class GovernorOutcome(StrEnum):
    """Canonical operational governance outcomes."""

    APPROVED = "approved"
    DENIED = "denied"
    DEFERRED = "deferred"
    THROTTLED = "throttled"
    ESCALATED = "escalated"


class GovernorMode(StrEnum):
    """Canonical governor operating modes."""

    NORMAL = "normal"
    FROZEN = "frozen"
    MAINTENANCE = "maintenance"
    EMERGENCY = "emergency"


@dataclass(frozen=True, slots=True)
class GovernorConstraints:
    """Bounded operational constraints."""

    maximum_restarts_per_target: int = 3
    maximum_concurrent_targets: int = 8
    restart_cooldown: timedelta = timedelta(0)
    manual_approval_for: frozenset[
        ExecutiveDecision
    ] = frozenset(
        {
            ExecutiveDecision.STOP_RUNTIME,
            ExecutiveDecision.ESCALATE,
            ExecutiveDecision.REQUIRE_MANUAL_ACTION,
        }
    )

    def __post_init__(self) -> None:
        if self.maximum_restarts_per_target < 0:
            raise ValueError(
                "maximum_restarts_per_target cannot be negative."
            )

        if self.maximum_concurrent_targets < 1:
            raise ValueError(
                "maximum_concurrent_targets must be positive."
            )

        if self.restart_cooldown < timedelta(0):
            raise ValueError(
                "restart_cooldown cannot be negative."
            )


@dataclass(frozen=True, slots=True)
class GovernorRequest:
    """Immutable request to govern an executive plan."""

    request_id: UUID
    generated_at: datetime
    plan: ExecutiveRecoveryPlan
    requested_by: str
    metadata: Mapping[str, Any]

    @classmethod
    def create(
        cls,
        *,
        plan: ExecutiveRecoveryPlan,
        requested_by: str = "constitutional-runtime-executive",
        metadata: Mapping[str, Any] | None = None,
    ) -> GovernorRequest:
        return cls(
            request_id=uuid4(),
            generated_at=datetime.now(UTC),
            plan=plan,
            requested_by=requested_by,
            metadata=MappingProxyType(
                dict(metadata or {})
            ),
        )


@dataclass(frozen=True, slots=True)
class GovernorDecision:
    """Immutable operational governance decision."""

    decision_id: UUID
    generated_at: datetime
    request_id: UUID
    outcome: GovernorOutcome
    approved: bool
    reason: str
    governed_action: ExecutiveDecision
    target_services: tuple[str, ...]
    requires_manual_approval: bool
    retry_after: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        request: GovernorRequest,
        outcome: GovernorOutcome,
        approved: bool,
        reason: str,
        requires_manual_approval: bool,
        retry_after: datetime | None = None,
    ) -> GovernorDecision:
        return cls(
            decision_id=uuid4(),
            generated_at=datetime.now(UTC),
            request_id=request.request_id,
            outcome=outcome,
            approved=approved,
            reason=reason,
            governed_action=request.plan.decision,
            target_services=tuple(
                sorted(request.plan.target_services)
            ),
            requires_manual_approval=(
                requires_manual_approval
            ),
            retry_after=retry_after,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": str(self.decision_id),
            "generated_at": (
                self.generated_at.isoformat()
            ),
            "request_id": str(self.request_id),
            "outcome": self.outcome.value,
            "approved": self.approved,
            "reason": self.reason,
            "governed_action": (
                self.governed_action.value
            ),
            "target_services": list(
                self.target_services
            ),
            "requires_manual_approval": (
                self.requires_manual_approval
            ),
            "retry_after": (
                self.retry_after.isoformat()
                if self.retry_after
                else None
            ),
        }


@dataclass(frozen=True, slots=True)
class GovernorStatistics:
    """Immutable governor statistics."""

    evaluations: int
    approvals: int
    denials: int
    deferrals: int
    throttles: int
    escalations: int
    frozen: bool
    quarantined_services: int

    def to_dict(self) -> dict[str, int | bool]:
        return {
            "evaluations": self.evaluations,
            "approvals": self.approvals,
            "denials": self.denials,
            "deferrals": self.deferrals,
            "throttles": self.throttles,
            "escalations": self.escalations,
            "frozen": self.frozen,
            "quarantined_services": (
                self.quarantined_services
            ),
        }
