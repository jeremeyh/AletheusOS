"""
AletheusOS
Genesis 49.0

Reason Engine™

Core Services
"""

from __future__ import annotations

from .evaluation import reason_evaluation
from .inference import reason_inference
from .justification import reason_justification
from .models import (
    ReasonObject,
    ReasonStatus,
    new_reason_id,
)
from .registry import reason_registry


class ReasonEngine:
    """
    Constitutional Reason Engine.

    The Reason Engine transforms
    constitutional context into an
    explainable conclusion.

    Pipeline

        Infer

            ↓

        Justify

            ↓

        Evaluate

            ↓

        Register
    """

    GENESIS = "49.0"
    VERSION = "1.0.0"

    def reason(
        self,
        *,
        intent: str,
        identity: str,
        query: str,
        conclusion: str,
        evidence: list[str] | None = None,
        memories_used: list[str] | None = None,
        constitutional_articles: list[str] | None = None,
        confidence: float = 0.0,
        provenance: dict | None = None,
        metadata: dict | None = None,
    ) -> ReasonObject:

        #
        # Candidate inference
        #

        alternatives = reason_inference.infer(
            query=query,
            evidence=evidence,
            memories=memories_used,
        )

        #
        # Build constitutional object
        #

        reason = ReasonObject(
            reason_id=new_reason_id(),
            intent=intent,
            identity=identity,
            query=query,
            conclusion=conclusion,
            evidence=evidence or [],
            memories_used=memories_used or [],
            alternatives_considered=alternatives,
            constitutional_articles=constitutional_articles or [],
            provenance=provenance or {},
            metadata=metadata or {},
        )

        reason.set_confidence(confidence)

        reason.set_status(ReasonStatus.INFERRED)

        #
        # Constitutional justification
        #

        reason_justification.justify(reason)

        #
        # Constitutional evaluation
        #

        reason_evaluation.evaluate(reason)

        #
        # Register reasoning
        #

        if reason.status == ReasonStatus.EVALUATED:
            reason.set_status(ReasonStatus.COMPLETED)

        reason_registry.register(reason)

        return reason

    def health(self) -> dict:

        return {
            "name": "Reason Engine",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
            "registry": reason_registry.health(),
            "inference": reason_inference.health(),
            "justification": reason_justification.health(),
            "evaluation": reason_evaluation.health(),
        }

    def statistics(self) -> dict:

        return reason_registry.statistics()


reason_engine = ReasonEngine()
