"""Integrity score calculation."""

from __future__ import annotations

from collections import Counter
from typing import Any

from .models import IntegrityDimension


def _status(score: float) -> str:
    if score >= 90:
        return "healthy"
    if score >= 75:
        return "watch"
    if score >= 60:
        return "degraded"
    return "critical"


def _dimension(name: str, score: float, deductions: list[str]) -> IntegrityDimension:
    bounded = round(max(0.0, min(100.0, score)), 2)
    return IntegrityDimension(
        name=name,
        score=bounded,
        status=_status(bounded),
        deductions=tuple(deductions),
    )


def score_repository(repository: dict[str, Any]) -> list[IntegrityDimension]:
    findings = repository.get("findings", [])
    if not isinstance(findings, list):
        raise TypeError("Repository report findings must be a list.")

    codes = Counter(
        str(item.get("code", "UNKNOWN")) for item in findings if isinstance(item, dict)
    )

    syntax_count = codes["SYNTAX_ERROR"]
    boundary_count = codes["BOUNDARY_VIOLATION"]
    duplicate_count = codes["EXACT_STRUCTURAL_DUPLICATE"]
    orphan_count = codes["ORPHAN_CANDIDATE"]

    return [
        _dimension(
            "syntax",
            100 - syntax_count * 20,
            [f"{syntax_count} syntax error(s)"] if syntax_count else [],
        ),
        _dimension(
            "boundaries",
            100 - boundary_count * 10,
            [f"{boundary_count} boundary violation(s)"] if boundary_count else [],
        ),
        _dimension(
            "duplication",
            100 - duplicate_count * 2,
            [f"{duplicate_count} exact structural duplicate(s)"]
            if duplicate_count
            else [],
        ),
        _dimension(
            "reachability",
            100 - orphan_count * 0.25,
            [f"{orphan_count} orphan candidate(s)"] if orphan_count else [],
        ),
    ]


def score_resolution(resolution: dict[str, Any]) -> IntegrityDimension:
    items = resolution.get("items", [])
    if not isinstance(items, list):
        raise TypeError("Resolution report items must be a list.")

    tiers = Counter(
        str(item.get("tier", "unknown")) for item in items if isinstance(item, dict)
    )
    score = 100 - tiers["critical"] * 20 - tiers["high"] * 8 - tiers["medium"] * 1
    deductions = [
        f"{tiers['critical']} critical",
        f"{tiers['high']} high",
        f"{tiers['medium']} medium",
    ]
    return _dimension("resolution", score, deductions)


def score_package_health(repository: dict[str, Any]) -> IntegrityDimension:
    metrics = repository.get("package_metrics", [])
    if not isinstance(metrics, list):
        raise TypeError("Repository package_metrics must be a list.")

    scores = [
        float(item.get("health_score", 0)) for item in metrics if isinstance(item, dict)
    ]
    average = sum(scores) / len(scores) if scores else 0.0
    deductions = [] if average >= 90 else [f"Average package health is {average:.2f}"]
    return _dimension("package_health", average, deductions)
