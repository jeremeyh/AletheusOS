from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class RuntimeEngineState:
    engine_id: str
    status: str = "registered"
    enabled: bool = True
    last_action: str = "registered"
    metadata: dict[str, Any] = field(default_factory=dict)
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self):
        return {
            "engine_id": self.engine_id,
            "status": self.status,
            "enabled": self.enabled,
            "last_action": self.last_action,
            "metadata": self.metadata,
            "updated_at": self.updated_at,
        }
