from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class StateTransition:
    previous: str
    current: str
    reason: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self):
        return {
            "previous": self.previous,
            "current": self.current,
            "reason": self.reason,
            "timestamp": self.timestamp,
        }


@dataclass(slots=True)
class PlatformLifecycleResult:
    action: str
    state: str
    success: bool
    message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "action": self.action,
            "state": self.state,
            "success": self.success,
            "message": self.message,
            "metadata": self.metadata,
            "timestamp": datetime.now(UTC).isoformat(),
        }
