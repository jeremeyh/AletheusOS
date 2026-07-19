"""Execution contracts for the Constitutional Mission Runtime™."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class PhaseExecutionRequest:
    """Input presented to one bounded institutional phase executor."""

    mission_id: str
    case_id: str
    correlation_id: str
    phase_id: str
    institution_id: str

    inputs: dict[str, Any]
    context: dict[str, Any]


@dataclass(frozen=True, slots=True)
class PhaseExecutionResult:
    """
    Result returned by one institutional phase executor.

    `domain_event_type` identifies the semantic constitutional event produced
    by the institution. The Mission Runtime publishes that event through the
    Constitutional Event Fabric.

    TIME™ remains responsible only for phase progression.
    """

    institution_id: str
    phase_id: str
    evidence_type: str
    evidence: dict[str, Any]

    successful: bool = True
    message: str = ""

    domain_event_type: Any | None = None
    domain_event_tags: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "institution_id": self.institution_id,
            "phase_id": self.phase_id,
            "evidence_type": self.evidence_type,
            "evidence": dict(self.evidence),
            "successful": self.successful,
            "message": self.message,
            "domain_event_type": self.domain_event_type,
            "domain_event_tags": list(
                self.domain_event_tags
            ),
        }


class InstitutionPhaseExecutor(Protocol):
    """Contract implemented by bounded institutional phase executors."""

    institution_id: str

    def execute(
        self,
        request: PhaseExecutionRequest,
    ) -> PhaseExecutionResult:
        ...
