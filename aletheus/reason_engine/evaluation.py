"""
AletheusOS
Genesis 49.0

Reason Engine™

Evaluation
"""

from __future__ import annotations

from .models import (
    ReasonObject,
    ReasonStatus,
)


class ReasonEvaluation:
    """
    Constitutional Evaluation.

    Evaluation determines whether a
    justified conclusion satisfies
    constitutional expectations.

    Evaluation does not create reasoning.

    Evaluation governs reasoning.
    """

    GENESIS = "49.0"
    VERSION = "1.0.0"

    MINIMUM_CONFIDENCE = 0.50

    def evaluate(
        self,
        reason: ReasonObject,
    ) -> ReasonObject:

        #
        # Evidence must exist.
        #

        if not reason.evidence:

            reason.set_status(
                ReasonStatus.REJECTED
            )

            return reason

        #
        # Constitutional support must exist.
        #

        if not reason.constitutional_articles:

            reason.set_status(
                ReasonStatus.REJECTED
            )

            return reason

        #
        # Confidence threshold.
        #

        if reason.confidence < self.MINIMUM_CONFIDENCE:

            reason.set_status(
                ReasonStatus.REJECTED
            )

            return reason

        #
        # Reason chain should exist.
        #

        if not reason.reason_chain:

            reason.set_status(
                ReasonStatus.REJECTED
            )

            return reason

        #
        # Constitutional evaluation passed.
        #

        reason.set_status(
            ReasonStatus.EVALUATED
        )

        return reason

    def health(self) -> dict:

        return {
            "name": "Reason Evaluation",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
        }


reason_evaluation = ReasonEvaluation()
