from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class ExecutionStep:
    step: str
    source: str
    status: str = "completed"
    timestamp: str = field(default_factory=_timestamp)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "step": self.step,
            "source": self.source,
            "status": self.status,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }
