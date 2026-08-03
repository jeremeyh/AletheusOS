from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class HealthStatus(StrEnum):
    """Canonical health states for runtime-managed components."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class HealthReport:
    """Immutable health report returned by runtime components."""

    component_id: str
    status: HealthStatus
    summary: str
    details: Mapping[str, Any] = field(default_factory=dict)

    @property
    def is_available(self) -> bool:
        """True when the component can still participate in runtime operations."""
        return self.status in {
            HealthStatus.HEALTHY,
            HealthStatus.DEGRADED,
        }
