"""Platform Digital Twin statistics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlatformDigitalTwinStatistics:
    """Immutable Digital Twin operational statistics."""

    revision: int
    snapshots_retained: int
    events_observed: int
    services: int
    nodes: int
    relationships: int
    healthy: int
    warning: int
    degraded: int
    critical: int
    offline: int
    unknown: int

    def to_dict(self) -> dict[str, int]:
        return {
            "revision": self.revision,
            "snapshots_retained": (
                self.snapshots_retained
            ),
            "events_observed": (
                self.events_observed
            ),
            "services": self.services,
            "nodes": self.nodes,
            "relationships": self.relationships,
            "healthy": self.healthy,
            "warning": self.warning,
            "degraded": self.degraded,
            "critical": self.critical,
            "offline": self.offline,
            "unknown": self.unknown,
        }
