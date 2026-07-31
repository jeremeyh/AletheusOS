"""Canonical models for Constitutional Cognition™."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4


def new_cognition_id() -> str:
    return f"COGNITION-{uuid4().hex[:12].upper()}"


class ConstitutionalVirtue(StrEnum):
    TRUTH = "truth"
    INTEGRITY = "integrity"
    HUMILITY = "humility"
    COMPASSION = "compassion"
    KINDNESS = "kindness"
    AGAPE = "agape"
    JUSTICE = "justice"
    WISDOM = "wisdom"


class ContributionStance(StrEnum):
    SUPPORT = "support"
    CHALLENGE = "challenge"
    ABSTAIN = "abstain"


class ConvergenceState(StrEnum):
    CONVERGED = "converged"
    CONTESTED = "contested"
    INSUFFICIENT = "insufficient"
    FAILED = "failed"


class CognitiveSignalType(StrEnum):
    MESH_STARTED = "mesh_started"
    ENGINE_STARTED = "engine_started"
    ENGINE_COMPLETED = "engine_completed"
    ENGINE_FAILED = "engine_failed"
    CONVERGENCE_STARTED = "convergence_started"
    CONVERGENCE_COMPLETED = "convergence_completed"
    VIRTUES_EVALUATED = "virtues_evaluated"
    MESH_COMPLETED = "mesh_completed"


@dataclass(frozen=True, slots=True)
class EngineContribution:
    """One independent engine contribution to a cognitive question."""

    engine_id: str
    assertion_key: str
    stance: ContributionStance
    confidence: float

    evidence_count: int = 0
    weight: float = 1.0
    rationale: str = ""
    evidence: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Contribution confidence must be between 0.0 and 1.0.")

        if self.weight <= 0:
            raise ValueError("Contribution weight must be greater than zero.")

        if self.evidence_count < 0:
            raise ValueError("Evidence count may not be negative.")

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["stance"] = self.stance.value
        return value


@dataclass(frozen=True, slots=True)
class CognitiveSignal:
    signal_type: CognitiveSignalType
    cognition_id: str

    engine_id: str | None = None
    magnitude: float | None = None
    message: str = ""
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["signal_type"] = self.signal_type.value
        return value


@dataclass(frozen=True, slots=True)
class VirtueContext:
    """
    Observable facts used to evaluate constitutional behavior.

    These fields represent system behavior, not simulated emotion.
    """

    evidence_supported: bool = True
    provenance_complete: bool = True
    uncertainty_disclosed: bool = True
    human_impact_considered: bool = True
    communication_respectful: bool = True
    enduring_good_considered: bool = True
    rules_applied_consistently: bool = True
    long_term_consequences_considered: bool = True
    fabrication_detected: bool = False

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class VirtueFinding:
    virtue: ConstitutionalVirtue
    passed: bool
    score: float
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "virtue": self.virtue.value,
            "passed": self.passed,
            "score": self.score,
            "message": self.message,
        }


@dataclass(frozen=True, slots=True)
class VirtueAssessment:
    findings: tuple[VirtueFinding, ...]
    score: float
    passed: bool

    @property
    def violations(self) -> tuple[VirtueFinding, ...]:
        return tuple(finding for finding in self.findings if not finding.passed)

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "passed": self.passed,
            "violations": [finding.to_dict() for finding in self.violations],
            "findings": [finding.to_dict() for finding in self.findings],
        }


@dataclass(frozen=True, slots=True)
class ConvergenceResult:
    assertion_key: str
    state: ConvergenceState
    dominant_stance: ContributionStance | None

    confidence: float
    support_strength: float
    challenge_strength: float
    abstention_strength: float

    contributions: tuple[EngineContribution, ...]
    dissent: tuple[EngineContribution, ...]

    explanation: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "assertion_key": self.assertion_key,
            "state": self.state.value,
            "dominant_stance": (
                self.dominant_stance.value if self.dominant_stance else None
            ),
            "confidence": self.confidence,
            "support_strength": self.support_strength,
            "challenge_strength": self.challenge_strength,
            "abstention_strength": self.abstention_strength,
            "contributions": [item.to_dict() for item in self.contributions],
            "dissent": [item.to_dict() for item in self.dissent],
            "explanation": self.explanation,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class MeshExecutionReport:
    cognition_id: str
    assertion_key: str

    contributions: tuple[EngineContribution, ...]
    failures: tuple[dict[str, str], ...]
    convergence: ConvergenceResult
    virtues: VirtueAssessment
    signals: tuple[CognitiveSignal, ...]

    @property
    def successful(self) -> bool:
        return (
            self.convergence.state
            not in {
                ConvergenceState.FAILED,
                ConvergenceState.INSUFFICIENT,
            }
            and self.virtues.passed
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "cognition_id": self.cognition_id,
            "assertion_key": self.assertion_key,
            "successful": self.successful,
            "contributions": [item.to_dict() for item in self.contributions],
            "failures": list(self.failures),
            "convergence": self.convergence.to_dict(),
            "virtues": self.virtues.to_dict(),
            "signals": [signal.to_dict() for signal in self.signals],
        }
