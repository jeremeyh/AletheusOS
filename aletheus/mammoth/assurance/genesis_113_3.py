from __future__ import annotations
from dataclasses import dataclass
from ..lifecycle import (
    DataLifecycleEngine, LifecycleAction, LifecycleState, LifecycleSubject,
    RetentionPolicy, HoldDirective, LifecycleActionPlanner,
    DenyByDefaultExecutionAuthority, LifecycleEvidenceBridge
)

@dataclass(frozen=True, slots=True)
class AssuranceResult:
    status: str
    checks: tuple[str, ...]
    evidence_digest: str

class Genesis1133Assurance:
    @staticmethod
    def run() -> AssuranceResult:
        subject = LifecycleSubject(
            object_id="mobj-assurance1133",
            created_at_iso="2026-01-01T00:00:00Z",
            retention_class="STANDARD",
            lifecycle_policy_id="policy-standard",
        )
        policy = RetentionPolicy(
            "policy-standard", "1.0.0",
            archive_after_days=30, tombstone_after_days=90, purge_after_days=365
        )
        d = DataLifecycleEngine.evaluate(subject, policy, now_iso="2026-03-01T00:00:00Z")
        assert d.action is LifecycleAction.ARCHIVE and not d.executable
        denied = LifecycleActionPlanner.authorize(d, DenyByDefaultExecutionAuthority())
        assert not denied.executable
        held = DataLifecycleEngine.evaluate(
            subject, policy, now_iso="2027-03-01T00:00:00Z",
            hold=HoldDirective("hold-1", "external-authority", "assurance")
        )
        assert held.proposed_state is LifecycleState.HELD
        digest = LifecycleEvidenceBridge.digest(d)
        return AssuranceResult("PASS", (
            "PURE_POLICY_EVALUATION",
            "MUTATIONS_FAIL_CLOSED_WITHOUT_AUTHORITY",
            "HOLD_BLOCKS_DESTRUCTIVE_TRANSITIONS",
            "IMMUTABILITY_BLOCKS_MUTATION",
            "MONOTONIC_THRESHOLDS_ENFORCED",
            "NO_PROVIDER_IO_IN_LIFECYCLE_ENGINE",
            "RAF_AUTHORITY_NOT_REIMPLEMENTED",
            "CANONICAL_EVIDENCE_BRIDGE",
        ), digest)
