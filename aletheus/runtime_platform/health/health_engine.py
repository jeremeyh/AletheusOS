from __future__ import annotations

from datetime import UTC, datetime

from .health_model import (
    HealthEvidence,
    RuntimeHealth,
)


class HealthEngine:
    VERSION = "1.0.0"

    def evaluate(
        self,
        topology,
        providers,
    ) -> RuntimeHealth:

        evidence = []

        snapshot = providers.health()

        for name, data in snapshot.items():
            evidence.append(
                HealthEvidence(
                    source=name,
                    category="provider",
                    healthy=data.get(
                        "healthy",
                        False,
                    ),
                    message=data.get(
                        "status",
                        "unknown",
                    ),
                    metadata=data,
                )
            )

        healthy = all(item.healthy for item in evidence)

        return RuntimeHealth(
            healthy=healthy,
            evidence=tuple(evidence),
            timestamp=datetime.now(UTC).isoformat(),
        )
