from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    clamp,
    immutable_contract,
)


class Engine:
    """Execution Quality Analyzer capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.10.0"
    CAPABILITY: ClassVar[str] = "Execution Quality Analyzer"

    def analyze(
        self,
        mission: MissionSnapshot,
        correctness: float,
        timeliness: float,
        evidence_quality: float,
    ) -> dict[str, Any]:
        components = [clamp(correctness), clamp(timeliness), clamp(evidence_quality)]
        quality = sum(components) / len(components)
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "qualityScore": round(quality, 6),
                "qualityBand": "CRYSTALLINE" if quality >= 0.9 else "NEBULAR",
                "components": components,
            },
            mission,
            correctness,
            timeliness,
            evidence_quality,
        )
