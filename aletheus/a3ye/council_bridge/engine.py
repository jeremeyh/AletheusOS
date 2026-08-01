from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Thesis:
    engine_id: str
    position: str
    confidence: float
    rationale: str


class Engine:
    def deliberate(self, theses: tuple[Thesis, ...]) -> dict[str, object]:
        if not theses:
            return {
                "status": "NO_QUORUM",
                "majority": None,
                "minority": [],
                "thorxReady": False,
            }
        ranked = sorted(theses, key=lambda item: item.confidence, reverse=True)
        majority = ranked[0]
        minority = [
            {
                "engineId": item.engine_id,
                "position": item.position,
                "confidence": item.confidence,
                "rationale": item.rationale,
            }
            for item in ranked[1:]
            if item.position != majority.position
        ]
        return {
            "status": "CONSENSUS_WITH_QUALIFICATIONS" if minority else "CONSENSUS",
            "majority": {
                "engineId": majority.engine_id,
                "position": majority.position,
                "confidence": majority.confidence,
                "rationale": majority.rationale,
            },
            "minority": minority,
            "thorxReady": True,
        }
