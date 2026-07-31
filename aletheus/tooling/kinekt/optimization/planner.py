"""Candidate and work-package planning."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .models import OptimizationCandidate, WorkPackage
from .prioritizer import score


def _candidate(
    candidate_id: str,
    category: str,
    title: str,
    severity: str,
    effort: str,
    risk: str,
    confidence: float,
    gain: float,
    evidence: list[str],
) -> OptimizationCandidate:
    return OptimizationCandidate(
        candidate_id=candidate_id,
        category=category,
        title=title,
        severity=severity,
        effort=effort,
        risk=risk,
        confidence=confidence,
        expected_health_gain=round(gain, 2),
        priority_score=score(severity, effort, risk, confidence, gain),
        evidence=tuple(evidence),
    )


def candidates_from_reports(
    resolution: dict[str, Any],
    dependency: dict[str, Any],
    cohesion: dict[str, Any],
    boundary: dict[str, Any],
    health: dict[str, Any],
) -> tuple[list[OptimizationCandidate], list[str]]:
    candidates: list[OptimizationCandidate] = []
    abstentions: list[str] = []

    items = resolution.get("items", [])
    if isinstance(items, list):
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            tier = str(item.get("tier", "low"))
            if tier not in {"critical", "high", "medium"}:
                continue
            code = str(item.get("code", "UNKNOWN"))
            evidence = [
                str(value)
                for value in item.get("evidence", [])
                if isinstance(value, str)
            ][:50]
            category = "duplication" if "DUPLICATE" in code else "reachability"
            candidates.append(
                _candidate(
                    f"resolution-{index}",
                    category,
                    f"Resolve {code}: {item.get('subject', 'unknown')}",
                    tier,
                    "medium",
                    "medium",
                    float(item.get("confidence", 0.5)),
                    4.0 if tier == "critical" else 2.5 if tier == "high" else 1.0,
                    evidence,
                )
            )

    unresolved = dependency.get("unresolved_modules", [])
    if isinstance(unresolved, list) and unresolved:
        candidates.append(
            _candidate(
                "normalize-ownership",
                "ownership",
                f"Classify {len(unresolved)} unresolved modules",
                "high",
                "high",
                "low",
                0.92,
                min(12.0, len(unresolved) / 300.0),
                [str(value) for value in unresolved[:100]],
            )
        )

    packages = cohesion.get("packages", [])
    hotspots = (
        [
            item
            for item in packages
            if isinstance(item, dict)
            and item.get("status") in {"critical", "fragmented"}
        ]
        if isinstance(packages, list)
        else []
    )
    if hotspots:
        candidates.append(
            _candidate(
                "cohesion-hotspots",
                "cohesion",
                f"Remediate {len(hotspots)} cohesion hotspots",
                "high",
                "high",
                "medium",
                0.85,
                min(10.0, len(hotspots) / 50.0),
                [str(item.get("package")) for item in hotspots[:100]],
            )
        )

    findings = boundary.get("findings", [])
    high_findings = (
        [
            item
            for item in findings
            if isinstance(item, dict) and item.get("severity") == "high"
        ]
        if isinstance(findings, list)
        else []
    )
    if high_findings:
        candidates.append(
            _candidate(
                "boundary-remediation",
                "boundary",
                f"Resolve {len(high_findings)} high boundary findings",
                "critical",
                "high",
                "high",
                0.95,
                min(15.0, len(high_findings) * 1.5),
                [
                    f"{item.get('source')} -> {item.get('target')}"
                    for item in high_findings[:100]
                ],
            )
        )

    if str(health.get("readiness", "unknown")) == "not_ready":
        candidates.append(
            _candidate(
                "readiness-recovery",
                "governance",
                "Recover constitutional readiness",
                "high",
                "medium",
                "medium",
                0.90,
                8.0,
                ["Current readiness: not_ready"],
            )
        )

    if not candidates:
        abstentions.append("No supported optimization candidates were found.")

    return sorted(
        candidates, key=lambda item: (-item.priority_score, item.candidate_id)
    ), abstentions


def build_work_packages(candidates: list[OptimizationCandidate]) -> list[WorkPackage]:
    grouped: dict[str, list[OptimizationCandidate]] = defaultdict(list)
    for candidate in candidates:
        grouped[candidate.category].append(candidate)

    phases = {
        "ownership": 1,
        "boundary": 2,
        "duplication": 3,
        "cohesion": 3,
        "reachability": 4,
        "governance": 5,
    }
    packages: list[WorkPackage] = []
    for category, items in grouped.items():
        effort = "high" if any(i.effort == "high" for i in items) else "medium"
        risk = "high" if any(i.risk == "high" for i in items) else "medium"
        packages.append(
            WorkPackage(
                package_id=f"wp-{category}",
                title=f"{category.replace('_', ' ').title()} Optimization",
                phase=phases.get(category, 6),
                category=category,
                candidate_ids=tuple(i.candidate_id for i in items),
                estimated_effort=effort,
                risk=risk,
                expected_health_gain=round(
                    sum(i.expected_health_gain for i in items),
                    2,
                ),
            )
        )
    return sorted(packages, key=lambda item: (item.phase, item.package_id))
