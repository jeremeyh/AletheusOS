"""Factory for the SPAN™ capability."""

from __future__ import annotations

from .analyzer import SpectrumPlatformAnalyzer
from .capability import SPANCapability
from .config import SPANConfig
from .guidance import ConstitutionalGuidance
from .lifecycle import SPANLifecycle
from .memory import InMemoryStrategicMemory
from .navigator import PlatformNavigator
from .recommendation_engine import StrategicRecommendationEngine
from .telemetry import SPANTelemetry


def build_span(
    config: SPANConfig | None = None,
    *,
    spartan: object | None = None,
) -> SPANCapability:
    resolved_config = config or SPANConfig()
    resolved_config.validate()

    return SPANCapability(
        config=resolved_config,
        analyzer=SpectrumPlatformAnalyzer(),
        navigator=PlatformNavigator(),
        guidance=ConstitutionalGuidance(),
        recommendation_engine=StrategicRecommendationEngine(),
        memory=InMemoryStrategicMemory(),
        lifecycle=SPANLifecycle(),
        telemetry=SPANTelemetry(),
        spartan=spartan,
    )
