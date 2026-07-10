from __future__ import annotations

from aletheus.time_utils import utc_now, utc_now_iso
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

@dataclass
class RuntimeMetric:
    name: str
    value: Any
    timestamp: str = field(default_factory=lambda: utc_now_iso())
    def to_dict(self) -> Dict[str, Any]: return {"name": self.name, "value": self.value, "timestamp": self.timestamp}

class RuntimeMetrics:
    def __init__(self) -> None: self.metrics: List[RuntimeMetric] = []
    def record(self, name: str, value: Any) -> None: self.metrics.append(RuntimeMetric(name=name, value=value))
    def recent(self, limit: int = 100) -> List[Dict[str, Any]]: return [metric.to_dict() for metric in self.metrics[-limit:]]
    def count(self) -> int: return len(self.metrics)
