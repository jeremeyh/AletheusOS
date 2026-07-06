from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


def _timestamp():
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class MemoryRecord:
    memory_id: str
    ledger_id: str
    decision_trace_id: str
    certification_id: str
    application: str
    relix_profile: str
    recommendation: str
    confidence: float
    precedent_weight: str = "LOW"
    tags: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    entities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=_timestamp)

    def to_dict(self):
        return {
            "memory_id": self.memory_id,
            "ledger_id": self.ledger_id,
            "decision_trace_id": self.decision_trace_id,
            "certification_id": self.certification_id,
            "application": self.application,
            "relix_profile": self.relix_profile,
            "recommendation": self.recommendation,
            "confidence": self.confidence,
            "precedent_weight": self.precedent_weight,
            "tags": self.tags,
            "keywords": self.keywords,
            "entities": self.entities,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }
