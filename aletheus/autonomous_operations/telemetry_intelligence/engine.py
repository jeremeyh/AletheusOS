from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    TelemetrySample,
    immutable_contract,
)


class Engine:
    """Operational Telemetry Intelligence capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.13.0"
    CAPABILITY: ClassVar[str] = "Operational Telemetry Intelligence"

    def summarize(
        self,
        mission: MissionSnapshot,
        samples: list[TelemetrySample],
    ) -> dict[str, Any]:
        grouped: dict[str, list[float]] = {}
        for sample in samples:
            grouped.setdefault(sample.name, []).append(sample.value)
        summary = {
            name: {
                "count": len(values),
                "minimum": min(values),
                "maximum": max(values),
                "average": sum(values) / len(values),
            }
            for name, values in sorted(grouped.items())
        }
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "metrics": summary,
                "sampleCount": len(samples),
            },
            mission,
            samples,
        )
