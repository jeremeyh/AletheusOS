"""Behavioral contracts for SPAN™ components."""

from __future__ import annotations

from typing import Iterable, Protocol, runtime_checkable
from uuid import UUID

from .models import (
    AnalysisRequest,
    AnalysisResult,
    ConstitutionalAssessment,
    NavigationPlan,
    Recommendation,
)


@runtime_checkable
class Analyzer(Protocol):
    def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        """Analyze a platform subject and return traceable findings."""


@runtime_checkable
class Navigator(Protocol):
    def navigate(self, analysis: AnalysisResult) -> NavigationPlan:
        """Produce a bounded path from the current state to a target state."""


@runtime_checkable
class ConstitutionalGuide(Protocol):
    def assess(
        self,
        analysis: AnalysisResult,
        navigation: NavigationPlan,
    ) -> ConstitutionalAssessment:
        """Assess constitutional alignment before recommendation publication."""


@runtime_checkable
class RecommendationEngine(Protocol):
    def recommend(
        self,
        analysis: AnalysisResult,
        navigation: NavigationPlan,
        assessment: ConstitutionalAssessment,
    ) -> Recommendation:
        """Generate a prioritized, constitutionally assessed recommendation."""


@runtime_checkable
class StrategicMemory(Protocol):
    def record(self, recommendation: Recommendation) -> None:
        """Persist recommendation lineage and outcome context."""

    def get(self, recommendation_id: UUID) -> Recommendation | None:
        """Retrieve a recommendation by identifier."""

    def list(self) -> Iterable[Recommendation]:
        """List known recommendations."""


@runtime_checkable
class LifecycleParticipant(Protocol):
    @property
    def is_started(self) -> bool:
        """Return whether the participant is currently started."""

    def start(self) -> None:
        """Start the participant."""

    def stop(self) -> None:
        """Stop the participant."""
