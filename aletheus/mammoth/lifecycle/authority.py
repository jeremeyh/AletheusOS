from __future__ import annotations
from typing import Protocol
from .model import LifecycleDecision, LifecycleAction

class LifecyclePolicyAuthority(Protocol):
    """Resolves policy. It does not execute storage mutations."""
    def resolve(self, lifecycle_policy_id: str): ...

class LifecycleExecutionAuthority(Protocol):
    """External authority gate. Mammoth proposes; authority authorizes."""
    def authorize(self, decision: LifecycleDecision) -> str | None: ...

class DenyByDefaultExecutionAuthority:
    def authorize(self, decision: LifecycleDecision) -> str | None:
        if decision.action is LifecycleAction.RETAIN:
            return "non-mutating-retain"
        return None


# PASS_3A5J_TX04_CONTRADICTION_GUARD
def contradiction_guard(*, contradictory_evidence: bool, otherwise_authorized: bool) -> bool:
    """Fail-closed THORx authorization guard."""
    if contradictory_evidence:
        return False
    return bool(otherwise_authorized)
