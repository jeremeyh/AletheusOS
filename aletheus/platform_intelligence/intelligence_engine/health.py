"""Health analysis for the Platform Intelligence Engine."""

from __future__ import annotations

from aletheus.platform_intelligence.constitutional import (
    ConstitutionalHealth,
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

_HEALTH_WEIGHTS = {
    ConstitutionalHealth.HEALTHY: 100.0,
    ConstitutionalHealth.UNKNOWN: 70.0,
    ConstitutionalHealth.WARNING: 55.0,
    ConstitutionalHealth.DEGRADED: 30.0,
    ConstitutionalHealth.CRITICAL: 5.0,
    ConstitutionalHealth.OFFLINE: 0.0,
}


def analyze_health(
    explorer: RuntimeExplorer,
) -> tuple[
    float,
    tuple[PlatformInsight, ...],
    tuple[PlatformRecommendation, ...],
]:
    services = explorer.services()

    if not services:
        return 100.0, (), ()

    score = sum(
        _HEALTH_WEIGHTS[service.health]
        for service in services
    ) / len(services)

    insights: list[PlatformInsight] = []
    recommendations: list[
        PlatformRecommendation
    ] = []

    unhealthy = tuple(
        service
        for service in services
        if service.health
        in {
            ConstitutionalHealth.WARNING,
            ConstitutionalHealth.DEGRADED,
            ConstitutionalHealth.CRITICAL,
            ConstitutionalHealth.OFFLINE,
        }
    )

    for service in unhealthy:
        severity = (
            IntelligenceSeverity.CRITICAL
            if service.health
            in {
                ConstitutionalHealth.CRITICAL,
                ConstitutionalHealth.OFFLINE,
            }
            else IntelligenceSeverity.WARNING
        )

        impact = explorer.impact(service.address)

        insights.append(
            PlatformInsight.create(
                category=IntelligenceCategory.HEALTH,
                severity=severity,
                title=(
                    f"{service.canonical_name} health "
                    f"is {service.health.value}"
                ),
                description=(
                    "The service is outside its healthy "
                    "operational state."
                ),
                evidence={
                    "address": service.address,
                    "health": service.health.value,
                    "affected_count": (
                        impact.affected_count
                    ),
                },
                confidence=1.0,
            )
        )

        recommendations.append(
            PlatformRecommendation.create(
                category=IntelligenceCategory.HEALTH,
                severity=severity,
                title=(
                    f"Investigate {service.canonical_name}"
                ),
                action=(
                    "Inspect service metrics, dependencies, "
                    "and recent constitutional events."
                ),
                rationale=(
                    f"Current health is "
                    f"{service.health.value} with "
                    f"{impact.affected_count} potentially "
                    "affected dependents."
                ),
                subjects=(service.address,),
                confidence=0.95,
            )
        )

    unknown = tuple(
        service
        for service in services
        if service.health
        is ConstitutionalHealth.UNKNOWN
    )

    if unknown:
        insights.append(
            PlatformInsight.create(
                category=IntelligenceCategory.HEALTH,
                severity=IntelligenceSeverity.NOTICE,
                title="Services lack health evidence",
                description=(
                    "One or more registered services have "
                    "not reported constitutional health."
                ),
                evidence={
                    "services": [
                        service.address
                        for service in unknown
                    ],
                    "count": len(unknown),
                },
                confidence=1.0,
            )
        )

    return (
        round(score, 2),
        tuple(insights),
        tuple(recommendations),
    )
