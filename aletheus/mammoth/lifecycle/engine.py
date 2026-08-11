from __future__ import annotations
from datetime import datetime, timezone
from types import MappingProxyType
from .model import (
    LifecycleAction, LifecycleDecision, LifecycleState,
    LifecycleSubject, RetentionPolicy, HoldDirective
)

_MUTATING = {
    LifecycleAction.ARCHIVE,
    LifecycleAction.RELEASE_HOLD,
    LifecycleAction.TOMBSTONE,
    LifecycleAction.PURGE,
}

class DataLifecycleEngine:
    """Pure lifecycle evaluator. No provider I/O and no policy invention."""

    @staticmethod
    def _parse(iso: str) -> datetime:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    @classmethod
    def evaluate(
        cls,
        subject: LifecycleSubject,
        policy: RetentionPolicy,
        *,
        now_iso: str,
        hold: HoldDirective | None = None,
    ) -> LifecycleDecision:
        now = cls._parse(now_iso)
        created = cls._parse(subject.created_at_iso)
        if now < created:
            raise ValueError("now_iso cannot precede object creation")
        age_days = (now - created).total_seconds() / 86400.0

        action = LifecycleAction.RETAIN
        proposed = subject.current_state
        reason = "Object remains within lifecycle constraints."

        if hold and hold.active:
            if not policy.hold_allowed:
                raise ValueError("active hold supplied for policy that forbids holds")
            action = LifecycleAction.HOLD
            proposed = LifecycleState.HELD
            reason = f"Active hold {hold.hold_id} blocks destructive lifecycle actions."
        elif subject.current_state is LifecycleState.HELD:
            action = LifecycleAction.RETAIN
            proposed = LifecycleState.HELD
            reason = "Held object requires explicit hold-release authority."
        elif policy.immutable:
            reason = "Immutable policy blocks mutating lifecycle transitions."
        elif policy.purge_after_days is not None and age_days >= policy.purge_after_days:
            action = LifecycleAction.PURGE
            proposed = LifecycleState.PURGED
            reason = "Object reached purge eligibility threshold."
        elif policy.tombstone_after_days is not None and age_days >= policy.tombstone_after_days:
            action = LifecycleAction.TOMBSTONE
            proposed = LifecycleState.TOMBSTONED
            reason = "Object reached tombstone eligibility threshold."
        elif policy.archive_after_days is not None and age_days >= policy.archive_after_days:
            action = LifecycleAction.ARCHIVE
            proposed = LifecycleState.ARCHIVED
            reason = "Object reached archive eligibility threshold."

        return LifecycleDecision(
            object_id=subject.object_id,
            policy_id=policy.policy_id,
            policy_version=policy.policy_version,
            current_state=subject.current_state,
            proposed_state=proposed,
            action=action,
            executable=action not in _MUTATING,
            reason=reason,
            evaluated_at_iso=now.isoformat().replace("+00:00", "Z"),
            evidence=MappingProxyType({
                "ageDays": f"{age_days:.6f}",
                "retentionClass": subject.retention_class,
                "lifecyclePolicyId": subject.lifecycle_policy_id,
            }),
        )
