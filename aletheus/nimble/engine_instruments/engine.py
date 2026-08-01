from __future__ import annotations

from .models import PrimitiveDefinition


class Engine:
    NAMES = (
        "EvidenceEngine",
        "KnowledgeEngine",
        "ReasonEngine",
        "MemoryEngine",
        "BiasEngine",
        "RiskEngine",
        "PredictiveEngine",
    )

    def catalog(self) -> tuple[PrimitiveDefinition, ...]:
        return tuple(
            PrimitiveDefinition(
                name=n,
                layer="engine_instruments",
                purpose=f"Instrument surface for {n}.",
                props=("state", "evidence", "confidence", "status", "explanation"),
            )
            for n in self.NAMES
        )
