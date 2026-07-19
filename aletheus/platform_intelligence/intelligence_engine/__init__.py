"""Platform Intelligence Engine public API."""

from .architecture import analyze_architecture
from .engine import PlatformIntelligenceEngine
from .health import analyze_health
from .models import (
    IntelligenceCategory,
    IntelligenceSeverity,
    PlatformInsight,
    PlatformIntelligenceAnalysis,
    PlatformRecommendation,
)

__all__ = [
    "IntelligenceCategory",
    "IntelligenceSeverity",
    "PlatformInsight",
    "PlatformIntelligenceAnalysis",
    "PlatformIntelligenceEngine",
    "PlatformRecommendation",
    "analyze_architecture",
    "analyze_health",
]
