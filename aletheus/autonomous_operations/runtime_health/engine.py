from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    TelemetrySample,
    clamp,
    immutable_contract,
)


class Engine:
    """Runtime Health Intelligence capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.8.0"
    CAPABILITY: ClassVar[str] = "Runtime Health Intelligence"

    def assess(
        self,
        mission: MissionSnapshot,
        samples: list[TelemetrySample],
    ) -> dict[str, Any]:
        if not samples:
            score = 0.5
        else:
            normalized = [clamp(sample.value) for sample in samples]
            score = 1.0 - sum(normalized) / len(normalized)
        state = "HEALTHY" if score >= 0.75 else "DEGRADED"
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "healthScore": round(clamp(score), 6),
                "runtimeState": state,
                "sampleCount": len(samples),
            },
            mission,
            samples,
        )
