"""
AletheusOS
Genesis 49.0

Reason Engine™

Justification
"""

from __future__ import annotations

from .models import (
    ReasonObject,
    ReasonStatus,
)


class ReasonJustification:
    """
    Constitutional Justification.

    Justification transforms a candidate
    conclusion into an explainable
    constitutional conclusion.

    Justification never invents evidence.

    It explains why the available evidence,
    memories, and constitutional principles
    support a conclusion.
    """

    GENESIS = "49.0"
    VERSION = "1.0.0"

    def justify(
        self,
        reason: ReasonObject,
    ) -> ReasonObject:

        #
        # Build constitutional reason chain.
        #

        if reason.evidence:
            reason.add_step(
                statement="Evidence reviewed.",
                support=reason.evidence,
                confidence=reason.confidence,
            )

        if reason.memories_used:
            reason.add_step(
                statement="Relevant constitutional memory considered.",
                support=reason.memories_used,
                confidence=reason.confidence,
            )

        if reason.constitutional_articles:
            reason.add_step(
                statement="Constitutional principles applied.",
                support=reason.constitutional_articles,
                confidence=reason.confidence,
            )

        #
        # Final justification
        #

        reason.add_step(
            statement=f"Conclusion justified: {reason.conclusion}",
            confidence=reason.confidence,
        )

        reason.set_status(ReasonStatus.JUSTIFIED)

        return reason

    def health(self) -> dict:

        return {
            "name": "Reason Justification",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
        }


reason_justification = ReasonJustification()
