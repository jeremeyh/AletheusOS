"""Strategic recommendation generation for SPAN™."""

from __future__ import annotations

from .models import (
    AnalysisResult,
    ConstitutionalAssessment,
    NavigationPlan,
    Recommendation,
    RecommendationPriority,
    RiskLevel,
)


class StrategicRecommendationEngine:
    """Generates advisory recommendations from validated inputs."""

    def recommend(
        self,
        analysis: AnalysisResult,
        navigation: NavigationPlan,
        assessment: ConstitutionalAssessment,
    ) -> Recommendation:
        confidence = min(
            analysis.confidence,
            assessment.confidence,
        )

        if not assessment.aligned:
            priority = RecommendationPriority.IMPORTANT
            risk_level = RiskLevel.HIGH
            title = "Resolve constitutional concerns before platform evolution"
        elif confidence >= 0.90:
            priority = RecommendationPriority.PLANNED
            risk_level = RiskLevel.LOW
            title = "Proceed to governed implementation planning"
        elif confidence >= 0.70:
            priority = RecommendationPriority.IMPORTANT
            risk_level = RiskLevel.MODERATE
            title = "Strengthen evidence before implementation"
        else:
            priority = RecommendationPriority.OBSERVE
            risk_level = RiskLevel.HIGH
            title = "Defer action pending stronger evidence"

        return Recommendation(
            title=title,
            rationale=(
                f"{analysis.summary} "
                f"Constitutional alignment: {assessment.aligned}. "
                f"Combined confidence: {confidence:.2f}."
            ),
            analysis=analysis,
            navigation=navigation,
            constitutional_assessment=assessment,
            priority=priority,
            risk_level=risk_level,
            confidence=confidence,
        )
