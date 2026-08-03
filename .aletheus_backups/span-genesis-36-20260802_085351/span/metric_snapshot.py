from dataclasses import dataclass
from datetime import UTC, datetime

from .metric_registry import MetricRegistry


@dataclass
class MetricSnapshot:
    registry: MetricRegistry
    created_at: datetime = datetime.now(UTC)
