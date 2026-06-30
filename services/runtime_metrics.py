from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any, Dict, List


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class RuntimeMetric:
    name: str
    value: Any
    tags: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=utc_now_iso)


class RuntimeMetrics:
    def __init__(self) -> None:
        self.metrics: List[RuntimeMetric] = []

    def record(self, name: str, value: Any, **tags: Any) -> None:
        self.metrics.append(RuntimeMetric(name=name, value=value, tags=tags))

    def recent(self, limit: int = 200) -> List[Dict[str, Any]]:
        return [asdict(m) for m in self.metrics[-limit:]]

    def latest_map(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        for metric in self.metrics:
            out[metric.name] = metric.value
        return out
