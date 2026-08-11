from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Mapping, Optional

class LifecycleState(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    HELD = "HELD"
    TOMBSTONED = "TOMBSTONED"
    PURGED = "PURGED"

class LifecycleAction(str, Enum):
    RETAIN = "RETAIN"
    ARCHIVE = "ARCHIVE"
    HOLD = "HOLD"
    RELEASE_HOLD = "RELEASE_HOLD"
    TOMBSTONE = "TOMBSTONE"
    PURGE = "PURGE"

@dataclass(frozen=True, slots=True)
class RetentionPolicy:
    policy_id: str
    policy_version: str
    retain_for_days: Optional[int] = None
    archive_after_days: Optional[int] = None
    tombstone_after_days: Optional[int] = None
    purge_after_days: Optional[int] = None
    immutable: bool = False
    hold_allowed: bool = True

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id is required")
        thresholds = [
            self.archive_after_days,
            self.tombstone_after_days,
            self.purge_after_days,
        ]
        values = [v for v in thresholds if v is not None]
        if any(v < 0 for v in values):
            raise ValueError("retention thresholds cannot be negative")
        if values != sorted(values):
            raise ValueError("lifecycle thresholds must be monotonic")

@dataclass(frozen=True, slots=True)
class HoldDirective:
    hold_id: str
    authority_ref: str
    reason: str
    active: bool = True

@dataclass(frozen=True, slots=True)
class LifecycleSubject:
    object_id: str
    created_at_iso: str
    retention_class: str
    lifecycle_policy_id: str
    current_state: LifecycleState = LifecycleState.ACTIVE

@dataclass(frozen=True, slots=True)
class LifecycleDecision:
    object_id: str
    policy_id: str
    policy_version: str
    current_state: LifecycleState
    proposed_state: LifecycleState
    action: LifecycleAction
    executable: bool
    reason: str
    evaluated_at_iso: str
    authority_ref: Optional[str] = None
    evidence: Mapping[str, str] = MappingProxyType({})
