"""Civilization Orchestrator result models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CivilizationResponse:
    """Complete outcome of one orchestrated constitutional response."""

    case_id: str
    mission_id: str
    security_case_id: str
    correlation_id: str

    case_status: str
    mission_status: str
    security_status: str

    evidence_count: int
    event_count: int

    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "mission_id": self.mission_id,
            "security_case_id": self.security_case_id,
            "correlation_id": self.correlation_id,
            "case_status": self.case_status,
            "mission_status": self.mission_status,
            "security_status": self.security_status,
            "evidence_count": self.evidence_count,
            "event_count": self.event_count,
            "metadata": dict(self.metadata),
        }
