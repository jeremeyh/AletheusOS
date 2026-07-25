"""Canonical SPAN™ domain models."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(UTC)


class RiskLevel(str, Enum):
    NEGLIGIBLE = "negligible"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class RecommendationPriority(str, Enum):
    OBSERVE = "observe"
    PLANNED = "planned"
    IMPORTANT = "important"
    URGENT = "urgent"
    CONSTITUTIONAL = "constitutional"


class RecommendationStatus(str, Enum):
    PROPOSED = "proposed"
    UNDER_REVIEW = "under_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    IMPLEMENTED = "implemented"
    VALIDATED = "validated"


@dataclass(frozen=True, slots=True)
class Evidence:
    source: str
    claim: str
    confidence: float
    observed_at: datetime = field(default_factory=utc_now)
    reference: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("Evidence source must not be empty")
        if not self.claim.strip():
            raise ValueError("Evidence claim must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Evidence confidence must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class AnalysisRequest:
    subject: str
    question: str
    requested_by: str
    context: Mapping[str, Any] = field(default_factory=dict)
    request_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.subject.strip():
            raise ValueError("Analysis subject must not be empty")
        if not self.question.strip():
            raise ValueError("Analysis question must not be empty")
        if not self.requested_by.strip():
            raise ValueError("requested_by must not be empty")


@dataclass(frozen=True, slots=True)
class ConstitutionalAssessment:
    aligned: bool
    principles_considered: tuple[str, ...]
    concerns: tuple[str, ...] = ()
    rationale: str = ""
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Assessment confidence must be between 0.0 and 1.0")
        if not self.principles_considered:
            raise ValueError("At least one constitutional principle is required")


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    request_id: UUID
    summary: str
    findings: tuple[str, ...]
    evidence: tuple[Evidence, ...]
    confidence: float
    risks: tuple[str, ...] = ()
    generated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.summary.strip():
            raise ValueError("Analysis summary must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Analysis confidence must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class NavigationPlan:
    current_state: str
    target_state: str
    steps: tuple[str, ...]
    dependencies: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    success_criteria: tuple[str, ...] = ()
    estimated_effort: str | None = None

    def __post_init__(self) -> None:
        if not self.current_state.strip():
            raise ValueError("current_state must not be empty")
        if not self.target_state.strip():
            raise ValueError("target_state must not be empty")
        if not self.steps:
            raise ValueError("Navigation plan requires at least one step")


@dataclass(frozen=True, slots=True)
class Recommendation:
    title: str
    rationale: str
    analysis: AnalysisResult
    navigation: NavigationPlan
    constitutional_assessment: ConstitutionalAssessment
    priority: RecommendationPriority
    risk_level: RiskLevel
    confidence: float
    status: RecommendationStatus = RecommendationStatus.PROPOSED
    recommendation_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Recommendation title must not be empty")
        if not self.rationale.strip():
            raise ValueError("Recommendation rationale must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Recommendation confidence must be between 0.0 and 1.0")
