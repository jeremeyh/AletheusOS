"""Constitutional guidance for SPAN™."""

from __future__ import annotations

from .models import (
    AnalysisResult,
    ConstitutionalAssessment,
    NavigationPlan,
)


class ConstitutionalGuidance:
    """Conservative constitutional assessment.

    This default guide does not claim access to the full Constitutional Graph.
    It checks baseline engineering principles until a platform adapter is wired.
    """

    _BASELINE_PRINCIPLES = (
        "Truth Precedes Intelligence™",
        "Evidence Precedes Knowledge™",
        "Governance Precedes Power™",
        "Stewardship Precedes Optimization™",
        "Human Agency Is Fundamental™",
        "Composition Over Accumulation™",
        "Boundaries Are Constitutional™",
    )

    def assess(
        self,
        analysis: AnalysisResult,
        navigation: NavigationPlan,
    ) -> ConstitutionalAssessment:
        concerns: list[str] = []

        if analysis.confidence < 0.70:
            concerns.append("Analysis confidence is below the preferred threshold.")
        if not analysis.evidence:
            concerns.append("No evidence artifacts were attached.")
        if not navigation.success_criteria:
            concerns.append("Navigation plan lacks measurable success criteria.")

        return ConstitutionalAssessment(
            aligned=not concerns,
            principles_considered=self._BASELINE_PRINCIPLES,
            concerns=tuple(concerns),
            rationale=(
                "Baseline constitutional assessment completed. "
                "A Constitutional Graph adapter should replace or augment this "
                "implementation when available."
            ),
            confidence=0.75 if concerns else 0.90,
        )
