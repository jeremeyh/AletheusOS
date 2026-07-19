"""SPAN™ composition root at the capability boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .analyzer import SpectrumPlatformAnalyzer
from .config import SPANConfig
from .guidance import ConstitutionalGuidance
from .lifecycle import SPANLifecycle
from .memory import InMemoryStrategicMemory
from .models import AnalysisRequest, Evidence, Recommendation
from .navigator import PlatformNavigator
from .recommendation_engine import StrategicRecommendationEngine
from .telemetry import SPANTelemetry


@dataclass(slots=True)
class SPANCapability:
    """Spectrum Platform Analyzer & Navigator™.

    SPAN is advisory by default. It analyzes, navigates, assesses, recommends,
    and records. It does not mutate AletheusOS™ directly.
    """

    config: SPANConfig
    analyzer: SpectrumPlatformAnalyzer
    navigator: PlatformNavigator
    guidance: ConstitutionalGuidance
    recommendation_engine: StrategicRecommendationEngine
    memory: InMemoryStrategicMemory
    lifecycle: SPANLifecycle
    telemetry: SPANTelemetry
    spartan: object | None = None

    @property
    def name(self) -> str:
        return self.config.capability_name

    @property
    def version(self) -> str:
        return self.config.capability_version

    @property
    def is_started(self) -> bool:
        return self.lifecycle.is_started

    def start(self) -> None:
        self.config.validate()
        if self.spartan is not None and hasattr(self.spartan, "start"):
            self.spartan.start()
        self.lifecycle.start()
        self.telemetry.increment("lifecycle.starts")

    def stop(self) -> None:
        if self.spartan is not None and hasattr(self.spartan, "stop"):
            self.spartan.stop()
        self.lifecycle.stop()
        self.telemetry.increment("lifecycle.stops")

    def evaluate(
        self,
        request: AnalysisRequest,
        evidence: Iterable[Evidence] = (),
    ) -> Recommendation:
        if not self.is_started:
            raise RuntimeError("SPAN must be started before evaluation")

        analysis = self.analyzer.analyze(request, evidence)
        self.telemetry.increment("analysis.completed")

        navigation = self.navigator.navigate(analysis)
        assessment = self.guidance.assess(analysis, navigation)
        recommendation = self.recommendation_engine.recommend(
            analysis,
            navigation,
            assessment,
        )

        if (
            recommendation.confidence
            >= self.config.minimum_recommendation_confidence
        ):
            self.memory.record(recommendation)
            self.telemetry.increment("recommendation.recorded")
        else:
            self.telemetry.increment("recommendation.withheld")

        self.telemetry.increment("recommendation.created")
        return recommendation
