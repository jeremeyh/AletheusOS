from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aletheus.time_utils import utc_now_iso


@dataclass
class RuntimeMetric:
    name: str
    value: Any
    timestamp: str = field(default_factory=lambda: utc_now_iso())

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "value": self.value, "timestamp": self.timestamp}


class RuntimeMetrics:
    def __init__(self) -> None:
        self.metrics: list[RuntimeMetric] = []

    def record(self, name: str, value: Any) -> None:
        self.metrics.append(RuntimeMetric(name=name, value=value))

    def recent(self, limit: int = 100) -> list[dict[str, Any]]:
        return [metric.to_dict() for metric in self.metrics[-limit:]]

    def count(self) -> int:
        return len(self.metrics)
