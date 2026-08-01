from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class CardIdentity:
    asset_id: str
    player: str
    sport: str
    year: int
    product: str
    card_number: str | None = None
    serial_number: str | None = None
    grade: str | None = None
    autograph: bool = False
    patch: bool = False


@dataclass(frozen=True)
class MarketObservation:
    source_id: str
    observation_type: str
    amount: float | None
    timestamp: str
    verified: bool
    reliability: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvidenceNode:
    node_id: str
    category: str
    value: Any
    confidence: float
    provenance: tuple[str, ...]
    temporal_class: str
    topology: str


@dataclass(frozen=True)
class DeterminationVector:
    veracity: float
    governance: float
    scarcity: float
    saturation: float
    momentum: float
    portfolio_fit: float
    downside_risk: float
    reason_density: float
    overall_strength: float

    def bounded(self) -> DeterminationVector:
        return DeterminationVector(
            **{key: min(1.0, max(0.0, value)) for key, value in asdict(self).items()}
        )


@dataclass(frozen=True)
class CardDetermination:
    asset: CardIdentity
    fair_value_low: float
    fair_value_mid: float
    fair_value_high: float
    decision: str
    vector: DeterminationVector
    evidence: tuple[EvidenceNode, ...] = ()
    disclosures: tuple[str, ...] = ()
    minority_views: tuple[str, ...] = ()
