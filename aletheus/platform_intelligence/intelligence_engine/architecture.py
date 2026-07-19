"""Architecture and topology analysis."""

from __future__ import annotations

from aletheus.platform_intelligence.constitutional_graph import (
    ConstitutionalGraph,
)
from aletheus.platform_intelligence.runtime_explorer import (
    RuntimeExplorer,
)

from .models import (
    IntelligenceCategory,
    IntelligenceSeverity,
    PlatformInsight,
    PlatformRecommendation,
)


def analyze_architecture(
    explorer: RuntimeExplorer,
    graph: ConstitutionalGraph,
    *,
    fan_in_warning_threshold: int = 5,
    depth_warning_threshold: int = 6,
) -> tuple[
    float,
    tuple[PlatformInsight, ...],
    tuple[PlatformRecommendation, ...],
]:
    stats = graph.statistics()
    score = 100.0

    insights: list[PlatformInsight] = []
    recommendations: list[
        PlatformRecommendation
    ] = []

    cycles = graph.cycles()

    if cycles:
        penalty = min(60.0, len(cycles) * 25.0)
        score -= penalty

        insights.append(
            PlatformInsight.create(
                category=IntelligenceCategory.ARCHITECTURE,
                severity=IntelligenceSeverity.CRITICAL,
                title="Constitutional dependency cycles detected",
                description=(
                    "Cyclic relationships compromise bounded "
                    "composition and predictable lifecycle order."
                ),
                evidence={
                    "cycles": [
                        [
                            str(address)
                            for address in cycle
                        ]
                        for cycle in cycles
                    ],
                    "count": len(cycles),
                },
                confidence=1.0,
            )
        )

        recommendations.append(
            PlatformRecommendation.create(
                category=IntelligenceCategory.ARCHITECTURE,
                severity=IntelligenceSeverity.CRITICAL,
                title="Break constitutional dependency cycles",
                action=(
                    "Introduce a stable interface, event boundary, "
                    "or extracted service to remove each cycle."
                ),
                rationale=(
                    "Acyclic dependency flow is required for "
                    "predictable composition and recovery."
                ),
                subjects=tuple(
                    sorted(
                        {
                            str(address)
                            for cycle in cycles
                            for address in cycle
                        }
                    )
                ),
                confidence=1.0,
            )
        )

    orphans = graph.orphans()

    if orphans:
        score -= min(20.0, len(orphans) * 3.0)

        insights.append(
            PlatformInsight.create(
                category=IntelligenceCategory.TOPOLOGY,
                severity=IntelligenceSeverity.NOTICE,
                title="Orphaned constitutional objects detected",
                description=(
                    "Objects without relationships may represent "
                    "unfinished integration or obsolete capability."
                ),
                evidence={
                    "objects": [
                        item.address
                        for item in orphans
                    ],
                    "count": len(orphans),
                },
                confidence=0.9,
            )
        )

        recommendations.append(
            PlatformRecommendation.create(
                category=IntelligenceCategory.TOPOLOGY,
                severity=IntelligenceSeverity.NOTICE,
                title="Review orphaned platform objects",
                action=(
                    "Connect each object to its governing, owning, "
                    "or dependency relationship, or retire it."
                ),
                rationale=(
                    "Every constitutional object should have an "
                    "explicit role within platform topology."
                ),
                subjects=tuple(
                    item.address
                    for item in orphans
                ),
                confidence=0.9,
            )
        )

    hotspots: list[tuple[str, int]] = []

    for node in graph.nodes():
        dependent_count = len(
            graph.dependents(node.address)
        )

        if dependent_count >= fan_in_warning_threshold:
            hotspots.append(
                (node.address, dependent_count)
            )

    if hotspots:
        score -= min(
            20.0,
            len(hotspots) * 5.0,
        )

        insights.append(
            PlatformInsight.create(
                category=IntelligenceCategory.DEPENDENCY,
                severity=IntelligenceSeverity.WARNING,
                title="High dependency concentration detected",
                description=(
                    "One or more objects have high inbound "
                    "dependency concentration."
                ),
                evidence={
                    "hotspots": [
                        {
                            "address": address,
                            "dependent_count": count,
                        }
                        for address, count in hotspots
                    ]
                },
                confidence=0.95,
            )
        )

        recommendations.append(
            PlatformRecommendation.create(
                category=IntelligenceCategory.DEPENDENCY,
                severity=IntelligenceSeverity.WARNING,
                title="Reduce dependency concentration",
                action=(
                    "Evaluate interface extraction, redundancy, "
                    "or bounded service decomposition."
                ),
                rationale=(
                    "High fan-in increases blast radius and "
                    "single-point-of-failure pressure."
                ),
                subjects=tuple(
                    address
                    for address, _ in hotspots
                ),
                confidence=0.9,
            )
        )

    if stats.maximum_depth > depth_warning_threshold:
        score -= min(
            20.0,
            (
                stats.maximum_depth
                - depth_warning_threshold
            )
            * 3.0,
        )

        insights.append(
            PlatformInsight.create(
                category=IntelligenceCategory.DEPENDENCY,
                severity=IntelligenceSeverity.WARNING,
                title="Deep dependency chain detected",
                description=(
                    "Platform dependency depth exceeds the "
                    "configured constitutional threshold."
                ),
                evidence={
                    "maximum_depth": stats.maximum_depth,
                    "threshold": depth_warning_threshold,
                },
                confidence=0.9,
            )
        )

    return (
        max(0.0, round(score, 2)),
        tuple(insights),
        tuple(recommendations),
    )
