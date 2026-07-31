"""Constitutional Runtime Executive public API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .exceptions import (
    ConstitutionalRuntimeExecutiveError,
    ExecutiveDecisionError,
    ExecutivePolicyError,
    RecoveryPlanError,
)
from .models import (
    ExecutiveContext,
    ExecutiveDecision,
    ExecutivePolicyResult,
    ExecutiveRecommendation,
    ExecutiveRecoveryPlan,
    ExecutiveRisk,
    ExecutiveStatistics,
)
from .policies import (
    CriticalRuntimePolicy,
    DegradedRuntimePolicy,
    ExecutivePolicy,
    HealthyRuntimePolicy,
    WarningRuntimePolicy,
    default_executive_policies,
)

if TYPE_CHECKING:
    from .executive import ConstitutionalRuntimeExecutive


def __getattr__(name: str) -> Any:
    """
    Lazily expose runtime implementation objects.

    The policy engine imports executive models and policies. Eagerly importing
    ConstitutionalRuntimeExecutive here would cause the executive module to
    import the policy engine while that engine is still initializing.
    """

    if name == "ConstitutionalRuntimeExecutive":
        from .executive import ConstitutionalRuntimeExecutive

        return ConstitutionalRuntimeExecutive

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))


__all__ = [
    "ConstitutionalRuntimeExecutive",
    "ConstitutionalRuntimeExecutiveError",
    "CriticalRuntimePolicy",
    "DegradedRuntimePolicy",
    "ExecutiveContext",
    "ExecutiveDecision",
    "ExecutiveDecisionError",
    "ExecutivePolicy",
    "ExecutivePolicyError",
    "ExecutivePolicyResult",
    "ExecutiveRecommendation",
    "ExecutiveRecoveryPlan",
    "ExecutiveRisk",
    "ExecutiveStatistics",
    "HealthyRuntimePolicy",
    "RecoveryPlanError",
    "WarningRuntimePolicy",
    "default_executive_policies",
]
