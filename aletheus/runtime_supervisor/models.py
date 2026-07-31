from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class SupervisorObservation:
    event_type: str
    source: str
    severity: str = "info"
    message: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self):
        return {
            "event_type": self.event_type,
            "source": self.source,
            "severity": self.severity,
            "message": self.message,
            "payload": self.payload,
            "timestamp": self.timestamp,
        }


@dataclass(slots=True)
class SupervisorDecision:
    action: str
    authorized: bool
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "action": self.action,
            "authorized": self.authorized,
            "reason": self.reason,
            "metadata": self.metadata,
        }
