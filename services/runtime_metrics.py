from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass
class RuntimeMetric:
    name: str
    value: Any
    tags: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=utc_now_iso)


class RuntimeMetrics:
    def __init__(self) -> None:
        self.metrics: list[RuntimeMetric] = []

    def record(self, name: str, value: Any, **tags: Any) -> None:
        self.metrics.append(RuntimeMetric(name=name, value=value, tags=tags))

    def recent(self, limit: int = 200) -> list[dict[str, Any]]:
        return [asdict(m) for m in self.metrics[-limit:]]

    def latest_map(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for metric in self.metrics:
            out[metric.name] = metric.value
        return out
