"""Platform Intelligence Engine façade."""

from __future__ import annotations

from aletheus.platform_intelligence.constitutional_graph import (
    ConstitutionalGraph,
)
from aletheus.platform_intelligence.runtime_explorer import (
    RuntimeExplorer,
)

from .architecture import analyze_architecture
from .health import analyze_health
from .models import (
    IntelligenceSeverity,
    PlatformIntelligenceAnalysis,
)


class PlatformIntelligenceEngine:
    """
    Deterministic reasoning layer over Platform Intelligence.

    The engine is read-only. It derives insights and recommendations without
    mutating the runtime, registry, graph, Digital Twin, or Event Bus.
    """

    def __init__(
        self,
        *,
        explorer: RuntimeExplorer,
        graph: ConstitutionalGraph,
        fan_in_warning_threshold: int = 5,
        depth_warning_threshold: int = 6,
    ) -> None:
        if fan_in_warning_threshold < 1:
            raise ValueError(
                "fan_in_warning_threshold must be positive."
            )

        if depth_warning_threshold < 1:
            raise ValueError(
                "depth_warning_threshold must be positive."
            )

        self._explorer = explorer
        self._graph = graph
        self._fan_in_warning_threshold = (
            fan_in_warning_threshold
        )
        self._depth_warning_threshold = (
            depth_warning_threshold
        )

    def analyze(
        self,
    ) -> PlatformIntelligenceAnalysis:
        health_score, health_insights, health_recommendations = (
            analyze_health(self._explorer)
        )

        (
            architecture_score,
            architecture_insights,
            architecture_recommendations,
        ) = analyze_architecture(
            self._explorer,
            self._graph,
            fan_in_warning_threshold=(
                self._fan_in_warning_threshold
            ),
            depth_warning_threshold=(
                self._depth_warning_threshold
            ),
        )

        constitutional_score = (
            health_score * 0.45
            + architecture_score * 0.55
        )

        insights = tuple(
            sorted(
                (
                    *health_insights,
                    *architecture_insights,
                ),
                key=lambda insight: (
                    self._severity_rank(
                        insight.severity
                    ),
                    insight.category.value,
                    insight.title,
                ),
            )
        )

        recommendations = tuple(
            sorted(
                (
                    *health_recommendations,
                    *architecture_recommendations,
                ),
                key=lambda recommendation: (
                    self._severity_rank(
                        recommendation.severity
                    ),
                    recommendation.category.value,
                    recommendation.title,
                ),
            )
        )

        risk_level = self._risk_level(
            constitutional_score,
            insights,
        )

        explorer_stats = (
            self._explorer.statistics()
        )
        graph_stats = self._graph.statistics()

        metrics = {
            "objects": explorer_stats.objects,
            "services": explorer_stats.services,
            "relationships": (
                explorer_stats.relationships
            ),
            "unhealthy": explorer_stats.unhealthy,
            "orphans": explorer_stats.orphans,
            "cycles": explorer_stats.cycles,
            "maximum_depth": (
                graph_stats.maximum_depth
            ),
            "connected_components": (
                graph_stats.connected_components
            ),
            "average_in_degree": (
                graph_stats.average_in_degree
            ),
            "average_out_degree": (
                graph_stats.average_out_degree
            ),
        }

        return PlatformIntelligenceAnalysis.create(
            twin_revision=(
                explorer_stats.twin_revision
            ),
            constitutional_score=(
                constitutional_score
            ),
            health_score=health_score,
            architecture_score=architecture_score,
            risk_level=risk_level,
            insights=insights,
            recommendations=recommendations,
            metrics=metrics,
        )

    @staticmethod
    def _risk_level(
        score: float,
        insights: tuple[object, ...],
    ) -> IntelligenceSeverity:
        severities = {
            getattr(insight, "severity", None)
            for insight in insights
        }

        if (
            IntelligenceSeverity.CRITICAL
            in severities
            or score < 40
        ):
            return IntelligenceSeverity.CRITICAL

        if (
            IntelligenceSeverity.ERROR
            in severities
            or score < 60
        ):
            return IntelligenceSeverity.ERROR

        if (
            IntelligenceSeverity.WARNING
            in severities
            or score < 80
        ):
            return IntelligenceSeverity.WARNING

        if score < 95:
            return IntelligenceSeverity.NOTICE

        return IntelligenceSeverity.INFO

    @staticmethod
    def _severity_rank(
        severity: IntelligenceSeverity,
    ) -> int:
        order = {
            IntelligenceSeverity.CRITICAL: 0,
            IntelligenceSeverity.ERROR: 1,
            IntelligenceSeverity.WARNING: 2,
            IntelligenceSeverity.NOTICE: 3,
            IntelligenceSeverity.INFO: 4,
        }

        return order[severity]
