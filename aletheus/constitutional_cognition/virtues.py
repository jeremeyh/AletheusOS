"""Constitutional Virtues Framework™."""

from __future__ import annotations

from collections.abc import Callable

from .models import (
    ConstitutionalVirtue,
    VirtueAssessment,
    VirtueContext,
    VirtueFinding,
)


VirtueEvaluator = Callable[
    [VirtueContext],
    tuple[bool, str],
]


class ConstitutionalVirtuesFramework:
    """
    Evaluate observable platform behavior against constitutional virtues.

    The framework does not claim that software feels emotion. It verifies
    whether system behavior remains aligned with constitutional principles.
    """

    VERSION = "0.1.0"

    def __init__(self) -> None:
        self._evaluators: dict[
            ConstitutionalVirtue,
            VirtueEvaluator,
        ] = {}

        self._install_canonical_evaluators()

    def register(
        self,
        virtue: ConstitutionalVirtue,
        evaluator: VirtueEvaluator,
        *,
        replace: bool = False,
    ) -> None:
        if virtue in self._evaluators and not replace:
            raise ValueError(
                f"Evaluator for {virtue.value!r} is already registered."
            )

        self._evaluators[virtue] = evaluator

    def evaluate(
        self,
        context: VirtueContext,
    ) -> VirtueAssessment:
        findings = []

        for virtue in ConstitutionalVirtue:
            evaluator = self._evaluators[virtue]
            passed, message = evaluator(context)

            findings.append(
                VirtueFinding(
                    virtue=virtue,
                    passed=passed,
                    score=1.0 if passed else 0.0,
                    message=message,
                )
            )

        score = (
            sum(item.score for item in findings)
            / len(findings)
        )

        return VirtueAssessment(
            findings=tuple(findings),
            score=round(score, 4),
            passed=all(
                finding.passed
                for finding in findings
            ),
        )

    def _install_canonical_evaluators(self) -> None:
        self.register(
            ConstitutionalVirtue.TRUTH,
            lambda context: (
                (
                    context.evidence_supported
                    and not context.fabrication_detected
                ),
                (
                    "The result is evidence-supported and contains "
                    "no detected fabrication."
                    if (
                        context.evidence_supported
                        and not context.fabrication_detected
                    )
                    else (
                        "Truth requirement failed: unsupported evidence "
                        "or fabrication was detected."
                    )
                ),
            ),
        )

        self.register(
            ConstitutionalVirtue.INTEGRITY,
            lambda context: (
                context.provenance_complete,
                (
                    "Evidence provenance is complete."
                    if context.provenance_complete
                    else "Evidence provenance is incomplete."
                ),
            ),
        )

        self.register(
            ConstitutionalVirtue.HUMILITY,
            lambda context: (
                context.uncertainty_disclosed,
                (
                    "Uncertainty is disclosed proportionately."
                    if context.uncertainty_disclosed
                    else "The result overstates certainty."
                ),
            ),
        )

        self.register(
            ConstitutionalVirtue.COMPASSION,
            lambda context: (
                context.human_impact_considered,
                (
                    "Human impact was considered."
                    if context.human_impact_considered
                    else "Human impact was not considered."
                ),
            ),
        )

        self.register(
            ConstitutionalVirtue.KINDNESS,
            lambda context: (
                context.communication_respectful,
                (
                    "Communication is respectful and constructive."
                    if context.communication_respectful
                    else "Communication is unnecessarily harmful."
                ),
            ),
        )

        self.register(
            ConstitutionalVirtue.AGAPE,
            lambda context: (
                context.enduring_good_considered,
                (
                    "The enduring good of affected people was considered."
                    if context.enduring_good_considered
                    else "Enduring human good was not considered."
                ),
            ),
        )

        self.register(
            ConstitutionalVirtue.JUSTICE,
            lambda context: (
                context.rules_applied_consistently,
                (
                    "Rules were applied consistently."
                    if context.rules_applied_consistently
                    else "The evaluation applied rules inconsistently."
                ),
            ),
        )

        self.register(
            ConstitutionalVirtue.WISDOM,
            lambda context: (
                context.long_term_consequences_considered,
                (
                    "Long-term consequences were considered."
                    if context.long_term_consequences_considered
                    else "Long-term consequences were not considered."
                ),
            ),
        )

    def health(self) -> dict:
        return {
            "name": "Constitutional Virtues Framework™",
            "version": self.VERSION,
            "status": "online",
            "virtues": len(self._evaluators),
            "registered": [
                virtue.value
                for virtue in self._evaluators
            ],
        }
