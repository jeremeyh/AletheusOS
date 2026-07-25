from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class IntentPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class IntentStatus(str, Enum):
    PROPOSED = "proposed"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Intent:
    """
    First-class runtime primitive for AletheusOS.

    Intent answers:
        Why is the system acting?
    """

    intent_id: str
    mission: str
    objective: str

    beneficiary: str = "unknown"
    priority: IntentPriority = IntentPriority.NORMAL
    status: IntentStatus = IntentStatus.PROPOSED

    constraints: list[str] = field(default_factory=list)
    success_metrics: list[str] = field(default_factory=list)
    constitutional_context: list[str] = field(default_factory=list)

    source: str = "unknown"
    steward: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
