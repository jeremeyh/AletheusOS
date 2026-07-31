"""Immutable models for the Constitutional Policy Engine."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from aletheus.platform_intelligence.constitutional_runtime_executive.models import (
    ExecutiveDecision,
    ExecutivePolicyResult,
    ExecutiveRisk,
)


class ConstitutionalPolicyEngineState(StrEnum):
    """Canonical CPE lifecycle states."""

    OPEN = "open"
    FROZEN = "frozen"


@dataclass(frozen=True, slots=True)
class PolicyEvaluation:
    """Immutable aggregate policy evaluation."""

    evaluation_id: UUID
    generated_at: datetime
    selected_decision: ExecutiveDecision
    selected_risk: ExecutiveRisk
    selected_confidence: float
    selected_reason: str
    affected_services: tuple[str, ...]
    matched_policy_id: str | None
    results: tuple[ExecutivePolicyResult, ...]

    @classmethod
    def create(
        cls,
        *,
        selected_decision: ExecutiveDecision,
        selected_risk: ExecutiveRisk,
        selected_confidence: float,
        selected_reason: str,
        affected_services: tuple[str, ...],
        matched_policy_id: str | None,
        results: tuple[ExecutivePolicyResult, ...],
    ) -> PolicyEvaluation:
        return cls(
            evaluation_id=uuid4(),
            generated_at=datetime.now(UTC),
            selected_decision=selected_decision,
            selected_risk=selected_risk,
            selected_confidence=selected_confidence,
            selected_reason=selected_reason,
            affected_services=tuple(sorted(affected_services)),
            matched_policy_id=matched_policy_id,
            results=results,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "evaluation_id": str(self.evaluation_id),
            "generated_at": (self.generated_at.isoformat()),
            "selected_decision": (self.selected_decision.value),
            "selected_risk": (self.selected_risk.value),
            "selected_confidence": (self.selected_confidence),
            "selected_reason": (self.selected_reason),
            "affected_services": list(self.affected_services),
            "matched_policy_id": (self.matched_policy_id),
            "results": [result.to_dict() for result in self.results],
        }


@dataclass(frozen=True, slots=True)
class PolicyEngineStatistics:
    """Immutable CPE statistics."""

    registered_policies: int
    evaluations: int
    matched_evaluations: int
    unmatched_evaluations: int
    policy_matches: int
    frozen: bool

    def to_dict(self) -> dict[str, int | bool]:
        return {
            "registered_policies": (self.registered_policies),
            "evaluations": self.evaluations,
            "matched_evaluations": (self.matched_evaluations),
            "unmatched_evaluations": (self.unmatched_evaluations),
            "policy_matches": (self.policy_matches),
            "frozen": self.frozen,
        }
