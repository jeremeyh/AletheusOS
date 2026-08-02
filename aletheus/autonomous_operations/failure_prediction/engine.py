from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    TelemetrySample,
    clamp,
    immutable_contract,
)


class Engine:
    """Failure Prediction Intelligence capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.4.0"
    CAPABILITY: ClassVar[str] = "Failure Prediction Intelligence"

    def predict(
        self,
        mission: MissionSnapshot,
        samples: list[TelemetrySample],
    ) -> dict[str, Any]:
        values = [sample.value for sample in samples]
        average = sum(values) / len(values) if values else 0.0
        slope = values[-1] - values[0] if len(values) > 1 else 0.0
        probability = clamp(
            0.45 * mission.risk + 0.35 * max(slope, 0.0) + 0.20 * clamp(average),
        )
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "failureProbability": round(probability, 6),
                "forecast": "IMMINENT" if probability >= 0.8 else "WATCH",
                "sampleCount": len(samples),
            },
            mission,
            samples,
        )
