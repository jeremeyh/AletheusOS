from __future__ import annotations

from dataclasses import dataclass

from .models import AuditReport, ImportEdge
from .rules import (
    DEFAULT_ARCHITECTURE_RULES,
    ArchitectureRules,
)


@dataclass(frozen=True, slots=True)
class BoundaryViolation:
    """One invalid dependency relationship."""

    source: str
    target: str
    line: int
    rule: str
    message: str


def _is_allowed_exception(
    source: str,
    target: str,
    rules: ArchitectureRules,
) -> bool:
    return (source, target) in rules.allowed_upward_dependencies


def _check_forbidden_dependency(
    edge: ImportEdge,
    rules: ArchitectureRules,
) -> BoundaryViolation | None:
    for forbidden in rules.forbidden_dependencies:
        if forbidden.matches(edge.source, edge.target):
            return BoundaryViolation(
                source=edge.source,
                target=edge.target,
                line=edge.line,
                rule="forbidden_dependency",
                message=forbidden.reason,
            )

    return None


def _check_layer_direction(
    edge: ImportEdge,
    rules: ArchitectureRules,
) -> BoundaryViolation | None:
    source_layer = rules.layer_for(edge.source)
    target_layer = rules.layer_for(edge.target)

    if source_layer is None or target_layer is None:
        return None

    if source_layer.name == target_layer.name:
        return None

    # Lower-level layers have larger ranks. Importing a smaller-rank layer
    # therefore represents an upward dependency.
    if target_layer.rank >= source_layer.rank:
        return None

    if _is_allowed_exception(edge.source, edge.target, rules):
        return None

    return BoundaryViolation(
        source=edge.source,
        target=edge.target,
        line=edge.line,
        rule="upward_dependency",
        message=(
            f"{source_layer.name} may not depend upward upon {target_layer.name}."
        ),
    )


def find_boundary_violations(
    imports: list[ImportEdge],
    rules: ArchitectureRules = DEFAULT_ARCHITECTURE_RULES,
) -> list[BoundaryViolation]:
    """Find explicit and layer-direction dependency violations."""

    violations: list[BoundaryViolation] = []
    seen: set[tuple[str, str, int, str]] = set()

    for edge in imports:
        if not edge.internal:
            continue

        forbidden = _check_forbidden_dependency(edge, rules)

        if forbidden is not None:
            key = (
                forbidden.source,
                forbidden.target,
                forbidden.line,
                forbidden.rule,
            )

            if key not in seen:
                seen.add(key)
                violations.append(forbidden)

            continue

        layer_violation = _check_layer_direction(edge, rules)

        if layer_violation is None:
            continue

        key = (
            layer_violation.source,
            layer_violation.target,
            layer_violation.line,
            layer_violation.rule,
        )

        if key not in seen:
            seen.add(key)
            violations.append(layer_violation)

    return sorted(
        violations,
        key=lambda violation: (
            violation.source,
            violation.line,
            violation.target,
            violation.rule,
        ),
    )


def analyze_boundaries(
    report: AuditReport,
    rules: ArchitectureRules = DEFAULT_ARCHITECTURE_RULES,
) -> list[BoundaryViolation]:
    """Analyze and record runtime architecture boundary violations."""

    violations = find_boundary_violations(
        report.imports,
        rules,
    )

    for violation in violations:
        report.add_finding(
            "error",
            violation.rule,
            (f"{violation.message} {violation.source} imports {violation.target}."),
            f"{violation.source}:{violation.line}",
            source=violation.source,
            target=violation.target,
            import_line=violation.line,
        )

    return violations
