from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from .models import GovernedEvidence


@dataclass(frozen=True)
class FusedIntent:
    vector: tuple[float, ...]
    modalities: tuple[str, ...]
    confidence: float
    uncertainty: float


class Engine:
    def fuse(
        self,
        semantic: tuple[float, ...],
        acoustic: tuple[float, ...] = (),
        contextual: tuple[float, ...] = (),
        evidence: tuple[GovernedEvidence, ...] = (),
    ) -> FusedIntent:
        combined = semantic + acoustic + contextual
        if not combined:
            raise ValueError("At least one vector is required")
        norm = sqrt(sum(value * value for value in combined)) or 1.0
        confidence = (
            sum(item.confidence for item in evidence) / len(evidence)
            if evidence
            else 0.5
        )
        return FusedIntent(
            tuple(value / norm for value in combined),
            tuple(sorted({item.modality for item in evidence})),
            confidence,
            1.0 - confidence,
        )
