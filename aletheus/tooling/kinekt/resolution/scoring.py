"""Evidence-based finding classification."""

from __future__ import annotations

from typing import Any

from .models import ResolutionItem
from .policy import ResolutionPolicy


def _paths(finding: dict[str, Any]) -> tuple[str, ...]:
    evidence = tuple(str(item) for item in finding.get("evidence", ()))
    return tuple(item for item in evidence if "/" in item or item.endswith(".py"))


def resolve_finding(
    finding: dict[str, Any],
    policy: ResolutionPolicy,
) -> ResolutionItem:
    code = str(finding.get("code", "UNKNOWN"))
    subject = str(finding.get("subject", "unknown"))
    evidence = tuple(str(item) for item in finding.get("evidence", ()))
    paths = _paths(finding)
    rationale: list[str] = []

    if paths and all(policy.path_is_suppressed(path) for path in paths):
        return ResolutionItem(
            code=code,
            subject=subject,
            tier="suppressed",
            confidence=0.98,
            disposition="ignore_noncanonical",
            recommendation="Exclude from canonical architecture triage.",
            rationale=("All path evidence is non-canonical or generated.",),
            evidence=evidence,
        )

    if code == "SYNTAX_ERROR":
        tier = "critical"
        confidence = 0.99
        disposition = "repair"
        recommendation = "Repair or explicitly quarantine the unparsable module."
        rationale.append("Active Python could not parse the module.")
    elif code == "BOUNDARY_VIOLATION":
        tier = "high"
        confidence = 0.95
        disposition = "architectural_review"
        recommendation = (
            "Review the dependency and route it through a canonical boundary."
        )
        rationale.append("Configured architecture boundary was crossed.")
    elif code == "EXACT_STRUCTURAL_DUPLICATE":
        tier = "medium"
        confidence = 0.90
        disposition = "canonical_selection_review"
        recommendation = (
            "Compare ownership, dependents, tests, and runtime registration; "
            "select one canonical implementation."
        )
        rationale.append("AST-equivalent definitions exist across source paths.")
    elif code == "ORPHAN_CANDIDATE":
        tier = "low"
        confidence = 0.55
        disposition = "reachability_review"
        recommendation = (
            "Check dynamic registration, CLI entry points, plugins, and external consumers "
            "before deprecation."
        )
        rationale.append("No internal static import was found.")
        rationale.append("Static analysis cannot prove runtime unreachability.")
    else:
        tier = "low"
        confidence = 0.35
        disposition = "manual_review"
        recommendation = "Review the finding with additional architectural evidence."
        rationale.append("No specialized resolution policy exists.")

    if any(path.startswith("aletheus/") for path in paths):
        confidence = min(1.0, confidence + 0.03)
        rationale.append("Evidence touches canonical Aletheus source.")

    return ResolutionItem(
        code=code,
        subject=subject,
        tier=tier,
        confidence=round(confidence, 2),
        disposition=disposition,
        recommendation=recommendation,
        rationale=tuple(rationale),
        evidence=evidence,
    )
