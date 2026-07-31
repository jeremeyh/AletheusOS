"""Constitutional Convergence™."""

from __future__ import annotations

from collections import defaultdict

from .models import (
    ContributionStance,
    ConvergenceResult,
    ConvergenceState,
    EngineContribution,
)


class ConstitutionalConvergenceEngine:
    """
    Synthesize independent engine contributions without hiding dissent.

    Convergence is not forced consensus. A result may remain contested when
    independent engines produce materially conflicting signals.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        contest_threshold: float = 0.15,
        minimum_contributions: int = 1,
    ) -> None:
        if not 0.0 <= contest_threshold <= 1.0:
            raise ValueError("contest_threshold must be between 0.0 and 1.0.")

        if minimum_contributions < 1:
            raise ValueError("minimum_contributions must be at least one.")

        self.contest_threshold = contest_threshold
        self.minimum_contributions = minimum_contributions
        self._evaluations = 0

    def converge(
        self,
        *,
        assertion_key: str,
        contributions: tuple[
            EngineContribution,
            ...,
        ],
    ) -> ConvergenceResult:
        self._evaluations += 1

        relevant = tuple(
            contribution
            for contribution in contributions
            if contribution.assertion_key == assertion_key
        )

        if len(relevant) < self.minimum_contributions:
            return ConvergenceResult(
                assertion_key=assertion_key,
                state=ConvergenceState.INSUFFICIENT,
                dominant_stance=None,
                confidence=0.0,
                support_strength=0.0,
                challenge_strength=0.0,
                abstention_strength=0.0,
                contributions=relevant,
                dissent=(),
                explanation=(
                    "Insufficient independent contributions "
                    "for constitutional convergence."
                ),
            )

        strengths: dict[
            ContributionStance,
            float,
        ] = defaultdict(float)

        for contribution in relevant:
            strengths[contribution.stance] += (
                contribution.confidence * contribution.weight
            )

        support = strengths[ContributionStance.SUPPORT]
        challenge = strengths[ContributionStance.CHALLENGE]
        abstain = strengths[ContributionStance.ABSTAIN]

        directional_total = support + challenge

        if directional_total == 0:
            return ConvergenceResult(
                assertion_key=assertion_key,
                state=ConvergenceState.INSUFFICIENT,
                dominant_stance=None,
                confidence=0.0,
                support_strength=round(support, 4),
                challenge_strength=round(challenge, 4),
                abstention_strength=round(abstain, 4),
                contributions=relevant,
                dissent=(),
                explanation=(
                    "All engines abstained; no directional "
                    "constitutional signal exists."
                ),
            )

        difference_ratio = abs(support - challenge) / directional_total

        if support >= challenge:
            dominant = ContributionStance.SUPPORT
            dominant_strength = support
        else:
            dominant = ContributionStance.CHALLENGE
            dominant_strength = challenge

        agreement = dominant_strength / directional_total

        average_confidence = sum(
            item.confidence
            for item in relevant
            if item.stance != ContributionStance.ABSTAIN
        ) / max(
            1,
            sum(item.stance != ContributionStance.ABSTAIN for item in relevant),
        )

        confidence = round(
            agreement * average_confidence,
            4,
        )

        contested = (
            support > 0 and challenge > 0 and difference_ratio <= self.contest_threshold
        )

        state = ConvergenceState.CONTESTED if contested else ConvergenceState.CONVERGED

        dissent = tuple(
            contribution
            for contribution in relevant
            if contribution.stance
            not in {
                dominant,
                ContributionStance.ABSTAIN,
            }
        )

        if contested:
            explanation = (
                "Independent engines remain materially divided. "
                "The dissenting signals are preserved."
            )
        elif dissent:
            explanation = (
                f"The mesh converged toward {dominant.value!r}, "
                "while preserving dissenting engine contributions."
            )
        else:
            explanation = (
                f"The mesh converged toward {dominant.value!r} "
                "without directional dissent."
            )

        return ConvergenceResult(
            assertion_key=assertion_key,
            state=state,
            dominant_stance=dominant,
            confidence=confidence,
            support_strength=round(
                support,
                4,
            ),
            challenge_strength=round(
                challenge,
                4,
            ),
            abstention_strength=round(
                abstain,
                4,
            ),
            contributions=relevant,
            dissent=dissent,
            explanation=explanation,
            metadata={
                "agreement": round(
                    agreement,
                    4,
                ),
                "difference_ratio": round(
                    difference_ratio,
                    4,
                ),
                "participant_count": len(relevant),
            },
        )

    def health(self) -> dict:
        return {
            "name": "Constitutional Convergence™",
            "version": self.VERSION,
            "status": "online",
            "evaluations": self._evaluations,
            "contest_threshold": (self.contest_threshold),
            "minimum_contributions": (self.minimum_contributions),
        }
