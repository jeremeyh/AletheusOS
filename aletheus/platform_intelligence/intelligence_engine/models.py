"""Immutable models produced by the Platform Intelligence Engine."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping
from uuid import UUID, uuid4


class IntelligenceSeverity(StrEnum):
    """Severity assigned to an insight or recommendation."""

    INFO = "info"
    NOTICE = "notice"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class IntelligenceCategory(StrEnum):
    """Canonical intelligence categories."""

    HEALTH = "health"
    ARCHITECTURE = "architecture"
    DEPENDENCY = "dependency"
    TOPOLOGY = "topology"
    GOVERNANCE = "governance"
    LIFECYCLE = "lifecycle"


@dataclass(frozen=True, slots=True)
class PlatformInsight:
    """Evidence-backed observation about AletheusOS."""

    insight_id: UUID
    category: IntelligenceCategory
    severity: IntelligenceSeverity
    title: str
    description: str
    evidence: Mapping[str, Any]
    confidence: float

    @classmethod
    def create(
        cls,
        *,
        category: IntelligenceCategory,
        severity: IntelligenceSeverity,
        title: str,
        description: str,
        evidence: Mapping[str, Any] | None = None,
        confidence: float = 1.0,
    ) -> "PlatformInsight":
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "Insight confidence must be between 0 and 1."
            )

        return cls(
            insight_id=uuid4(),
            category=category,
            severity=severity,
            title=title.strip(),
            description=description.strip(),
            evidence=MappingProxyType(
                dict(evidence or {})
            ),
            confidence=confidence,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "insight_id": str(self.insight_id),
            "category": self.category.value,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "evidence": dict(self.evidence),
            "confidence": self.confidence,
        }


@dataclass(frozen=True, slots=True)
class PlatformRecommendation:
    """Structured recommendation derived from platform evidence."""

    recommendation_id: UUID
    category: IntelligenceCategory
    severity: IntelligenceSeverity
    title: str
    action: str
    rationale: str
    subjects: tuple[str, ...]
    confidence: float

    @classmethod
    def create(
        cls,
        *,
        category: IntelligenceCategory,
        severity: IntelligenceSeverity,
        title: str,
        action: str,
        rationale: str,
        subjects: tuple[str, ...] = (),
        confidence: float = 1.0,
    ) -> "PlatformRecommendation":
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "Recommendation confidence must be between 0 and 1."
            )

        return cls(
            recommendation_id=uuid4(),
            category=category,
            severity=severity,
            title=title.strip(),
            action=action.strip(),
            rationale=rationale.strip(),
            subjects=tuple(sorted(subjects)),
            confidence=confidence,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "recommendation_id": str(
                self.recommendation_id
            ),
            "category": self.category.value,
            "severity": self.severity.value,
            "title": self.title,
            "action": self.action,
            "rationale": self.rationale,
            "subjects": list(self.subjects),
            "confidence": self.confidence,
        }


@dataclass(frozen=True, slots=True)
class PlatformIntelligenceAnalysis:
    """Immutable complete analysis of the running platform."""

    analysis_id: UUID
    generated_at: datetime
    twin_revision: int
    constitutional_score: float
    health_score: float
    architecture_score: float
    risk_level: IntelligenceSeverity
    insights: tuple[PlatformInsight, ...]
    recommendations: tuple[
        PlatformRecommendation,
        ...,
    ]
    metrics: Mapping[str, Any]

    @classmethod
    def create(
        cls,
        *,
        twin_revision: int,
        constitutional_score: float,
        health_score: float,
        architecture_score: float,
        risk_level: IntelligenceSeverity,
        insights: tuple[PlatformInsight, ...],
        recommendations: tuple[
            PlatformRecommendation,
            ...,
        ],
        metrics: Mapping[str, Any],
    ) -> "PlatformIntelligenceAnalysis":
        return cls(
            analysis_id=uuid4(),
            generated_at=datetime.now(UTC),
            twin_revision=twin_revision,
            constitutional_score=round(
                constitutional_score,
                2,
            ),
            health_score=round(
                health_score,
                2,
            ),
            architecture_score=round(
                architecture_score,
                2,
            ),
            risk_level=risk_level,
            insights=insights,
            recommendations=recommendations,
            metrics=MappingProxyType(dict(metrics)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "analysis_id": str(self.analysis_id),
            "generated_at": (
                self.generated_at.isoformat()
            ),
            "twin_revision": self.twin_revision,
            "constitutional_score": (
                self.constitutional_score
            ),
            "health_score": self.health_score,
            "architecture_score": (
                self.architecture_score
            ),
            "risk_level": self.risk_level.value,
            "insights": [
                insight.to_dict()
                for insight in self.insights
            ],
            "recommendations": [
                recommendation.to_dict()
                for recommendation
                in self.recommendations
            ],
            "metrics": dict(self.metrics),
        }
