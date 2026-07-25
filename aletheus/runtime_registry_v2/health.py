from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass
class HealthCheck:
    """
    Canonical health check result for any runtime component.
    """

    component_id: str

    healthy: bool = True

    score: int = 100

    message: str = "Healthy"

    warnings: list[str] = field(default_factory=list)

    metrics: dict[str, float] = field(default_factory=dict)

    timestamp: str = field(default_factory=utc_now)


class HealthMonitor:
    """
    Shared runtime health service.

    Every component in AletheusOS can publish a HealthCheck.
    SPA, Breadth, the Founder Console, and future services
    consume the same standardized health information.
    """

    def __init__(self):

        self._checks: dict[str, HealthCheck] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def publish(self, check: HealthCheck):

        self._checks[check.component_id] = check

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(self, component_id: str):

        return self._checks.get(component_id)

    def all(self):

        return list(self._checks.values())

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(self):

        total = len(self._checks)

        if total == 0:
            return {
                "status": "unknown",
                "score": 0,
                "healthy": 0,
                "degraded": 0,
            }

        healthy = sum(
            1 for c in self._checks.values() if c.healthy
        )

        degraded = total - healthy

        average = round(
            sum(c.score for c in self._checks.values()) / total,
            1,
        )

        if average >= 95:
            status = "excellent"

        elif average >= 85:
            status = "healthy"

        elif average >= 70:
            status = "warning"

        else:
            status = "critical"

        return {
            "status": status,
            "score": average,
            "healthy": healthy,
            "degraded": degraded,
            "components": total,
        }
