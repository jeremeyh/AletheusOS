"""Constitutional health scoring."""

from __future__ import annotations

from typing import Any

from .models import HealthDimension


def status(score: float) -> str:
    if score >= 90:
        return "healthy"
    if score >= 75:
        return "watch"
    if score >= 60:
        return "degraded"
    return "critical"


def _dimension(
    name: str,
    score: float,
    weight: float,
    evidence: list[str],
    risks: list[str],
) -> HealthDimension:
    bounded = round(max(0.0, min(100.0, score)), 2)
    return HealthDimension(
        name=name,
        score=bounded,
        weight=weight,
        status=status(bounded),
        evidence=tuple(evidence),
        risks=tuple(risks),
    )


def build_dimensions(
    integrity: dict[str, Any],
    topology: dict[str, Any],
    dependency: dict[str, Any],
    cohesion: dict[str, Any],
    boundary: dict[str, Any],
) -> list[HealthDimension]:
    integrity_score = float(integrity.get("total_score", 0.0))
    cohesion_score = float(cohesion.get("average_score", 0.0))

    boundary_findings = boundary.get("findings", [])
    if not isinstance(boundary_findings, list):
        raise TypeError("Boundary findings must be a list.")
    high_boundaries = sum(
        isinstance(item, dict) and item.get("severity") == "high"
        for item in boundary_findings
    )
    medium_boundaries = sum(
        isinstance(item, dict) and item.get("severity") == "medium"
        for item in boundary_findings
    )
    boundary_score = max(0.0, 100.0 - high_boundaries * 12 - medium_boundaries * 5)

    unresolved_modules = int(
        dependency.get("unresolved_modules", [])
        and len(dependency.get("unresolved_modules", []))
    )
    dependency_nodes = (
        len(dependency.get("nodes", []))
        if isinstance(dependency.get("nodes", []), list)
        else 0
    )
    unresolved_ratio = unresolved_modules / max(1, dependency_nodes)
    dependency_score = max(0.0, 100.0 - unresolved_ratio * 100.0)

    isolated_modules = (
        len(topology.get("isolated", []))
        if isinstance(topology.get("isolated", []), list)
        else 0
    )
    module_count = (
        len(topology.get("modules", []))
        if isinstance(topology.get("modules", []), list)
        else 0
    )
    isolated_ratio = isolated_modules / max(1, module_count)
    topology_score = max(0.0, 100.0 - isolated_ratio * 70.0)

    dependency_findings = dependency.get("findings", [])
    if not isinstance(dependency_findings, list):
        raise TypeError("Dependency findings must be a list.")
    policy_findings = len(dependency_findings)
    constitutional_risk_score = max(
        0.0,
        100.0
        - policy_findings * 10.0
        - high_boundaries * 8.0
        - medium_boundaries * 3.0,
    )

    return [
        _dimension(
            "integrity",
            integrity_score,
            0.25,
            [f"Platform integrity score: {integrity_score:.2f}"],
            ["Platform integrity is below healthy."] if integrity_score < 90 else [],
        ),
        _dimension(
            "cohesion",
            cohesion_score,
            0.20,
            [f"Repository cohesion score: {cohesion_score:.2f}"],
            ["Repository remains fragmented."] if cohesion_score < 75 else [],
        ),
        _dimension(
            "boundary_compliance",
            boundary_score,
            0.20,
            [
                f"{high_boundaries} high boundary finding(s)",
                f"{medium_boundaries} medium boundary finding(s)",
            ],
            ["High-severity boundary violations remain."] if high_boundaries else [],
        ),
        _dimension(
            "dependency_resolution",
            dependency_score,
            0.15,
            [
                f"{unresolved_modules} unresolved module(s)",
                f"{dependency_nodes} dependency node(s)",
            ],
            ["Semantic dependency ownership remains incomplete."]
            if unresolved_modules
            else [],
        ),
        _dimension(
            "topology_connectedness",
            topology_score,
            0.10,
            [
                f"{isolated_modules} isolated module(s)",
                f"{module_count} total topology module(s)",
            ],
            ["Static topology contains substantial isolation."]
            if isolated_ratio > 0.25
            else [],
        ),
        _dimension(
            "constitutional_risk",
            constitutional_risk_score,
            0.10,
            [f"{policy_findings} dependency policy finding(s)"],
            ["Constitutional policy findings remain."] if policy_findings else [],
        ),
    ]


def total_score(dimensions: list[HealthDimension]) -> float:
    return round(
        sum(dimension.score * dimension.weight for dimension in dimensions),
        2,
    )


def readiness(score: float, dimensions: list[HealthDimension]) -> str:
    has_critical = any(dimension.status == "critical" for dimension in dimensions)
    if score >= 85 and not has_critical:
        return "ready"
    if score >= 65:
        return "conditional"
    return "not_ready"
