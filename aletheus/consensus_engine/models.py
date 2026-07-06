from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class CouncilOpinion:
    engine_id: str
    score: float
    confidence: float
    recommendation: str
    evidence: list[dict[str, Any]] = field(default_factory=list)
    explanation: str = ""
    flags: list[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "engine_id": self.engine_id,
            "score": self.score,
            "confidence": self.confidence,
            "recommendation": self.recommendation,
            "evidence": self.evidence,
            "explanation": self.explanation,
            "flags": self.flags,
        }


@dataclass(slots=True)
class ConsensusResult:
    consensus_score: float
    consensus_confidence: float
    recommendation: str
    opinions: list[dict[str, Any]]
    minority_reports: list[dict[str, Any]] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self):
        return {
            "consensus_score": self.consensus_score,
            "consensus_confidence": self.consensus_confidence,
            "recommendation": self.recommendation,
            "opinions": self.opinions,
            "minority_reports": self.minority_reports,
            "flags": self.flags,
            "timestamp": self.timestamp,
        }
