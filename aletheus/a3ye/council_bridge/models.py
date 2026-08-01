from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class SignalEnvelope:
    signal_id: str
    modality: str
    payload: dict[str, Any]
    consent: bool
    provenance: tuple[str, ...] = ()
    confidence: float = 1.0


@dataclass(frozen=True)
class GovernedEvidence:
    evidence_id: str
    modality: str
    content: dict[str, Any]
    provenance: tuple[str, ...]
    confidence: float
    uncertainty: float
    policy_labels: tuple[str, ...] = ()


@dataclass(frozen=True)
class TemporalFrame:
    historical: dict[str, Any]
    present: dict[str, Any]
    projected: dict[str, Any]
    unknowns: tuple[str, ...] = ()


@dataclass(frozen=True)
class DeterminationVector:
    veracity: float
    governance: float
    predictive_stability: float
    principle_x: float
    constitutional_entropy: float
    overall_strength: float

    def bounded(self) -> DeterminationVector:
        return DeterminationVector(
            **{key: min(1.0, max(0.0, value)) for key, value in asdict(self).items()}
        )


@dataclass(frozen=True)
class A3yeResponse:
    response_id: str
    thesis: str
    determination: DeterminationVector
    evidence: tuple[GovernedEvidence, ...] = ()
    minority_opinions: tuple[str, ...] = ()
    disclosures: tuple[str, ...] = ()
    projections: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
