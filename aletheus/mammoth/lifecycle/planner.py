from __future__ import annotations
from dataclasses import replace
from .authority import LifecycleExecutionAuthority
from .model import LifecycleDecision, LifecycleAction

_MUTATING = {
    LifecycleAction.ARCHIVE,
    LifecycleAction.RELEASE_HOLD,
    LifecycleAction.TOMBSTONE,
    LifecycleAction.PURGE,
}

class LifecycleActionPlanner:
    """Turns evaluation into an authorized plan; still performs no provider I/O."""
    @staticmethod
    def authorize(
        decision: LifecycleDecision,
        authority: LifecycleExecutionAuthority,
    ) -> LifecycleDecision:
        if decision.action not in _MUTATING:
            return decision
        authority_ref = authority.authorize(decision)
        if not authority_ref:
            return decision
        return replace(decision, executable=True, authority_ref=authority_ref)


# PASS_3A5J_TX04_PLANNER_HELPER
def authorize_with_contradiction_guard(*, contradictory_evidence: bool, otherwise_authorized: bool) -> bool:
    from .authority import contradiction_guard
    return contradiction_guard(
        contradictory_evidence=contradictory_evidence,
        otherwise_authorized=otherwise_authorized,
    )
