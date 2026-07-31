from __future__ import annotations

from .models import ArchitectureHealth, AuditReport

MAXIMUM_DEDUCTIONS = {
    "syntax_errors": 30,
    "dependency_cycles": 30,
    "legacy_references": 25,
    "ownership_errors": 20,
    "other_errors": 20,
    "warnings": 15,
}


def _bounded(value: int, maximum: int) -> int:
    return min(max(value, 0), maximum)


def _grade(score: int) -> str:
    if score >= 95:
        return "A+"
    if score >= 90:
        return "A"
    if score >= 85:
        return "B+"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def calculate_health(report: AuditReport) -> ArchitectureHealth:
    """Calculate a transparent architecture-health score."""

    syntax_errors = sum(
        finding.category == "syntax" and finding.severity == "error"
        for finding in report.findings
    )

    ownership_errors = sum(
        finding.category
        in {
            "kernel_ownership",
            "boot_pipeline_ownership",
        }
        and finding.severity == "error"
        for finding in report.findings
    )

    categorized_error_ids = {
        id(finding)
        for finding in report.findings
        if finding.severity == "error"
        and finding.category
        in {
            "syntax",
            "dependency_cycle",
            "legacy_runtime",
            "kernel_ownership",
            "boot_pipeline_ownership",
        }
    }

    other_errors = sum(
        finding.severity == "error" and id(finding) not in categorized_error_ids
        for finding in report.findings
    )

    deductions = {
        "syntax_errors": _bounded(
            syntax_errors * 15,
            MAXIMUM_DEDUCTIONS["syntax_errors"],
        ),
        "dependency_cycles": _bounded(
            len(report.dependency_cycles) * 10,
            MAXIMUM_DEDUCTIONS["dependency_cycles"],
        ),
        "legacy_references": _bounded(
            len(report.legacy_references) * 10,
            MAXIMUM_DEDUCTIONS["legacy_references"],
        ),
        "ownership_errors": _bounded(
            ownership_errors * 10,
            MAXIMUM_DEDUCTIONS["ownership_errors"],
        ),
        "other_errors": _bounded(
            other_errors * 5,
            MAXIMUM_DEDUCTIONS["other_errors"],
        ),
        "warnings": _bounded(
            report.warnings * 2,
            MAXIMUM_DEDUCTIONS["warnings"],
        ),
    }

    score = max(0, 100 - sum(deductions.values()))

    internal_edges = sum(edge.internal for edge in report.imports)

    metrics: dict[str, int | float | str | None] = {
        "modules": len(report.modules),
        "total_lines": sum(module.lines for module in report.modules),
        "internal_import_edges": internal_edges,
        "dependency_cycles": len(report.dependency_cycles),
        "orphan_modules": len(report.orphan_modules),
        "kernel_constructors": len(report.kernel_constructors),
        "boot_pipeline_paths": len(report.boot_pipeline_calls),
        "legacy_references": len(report.legacy_references),
        "errors": report.errors,
        "warnings": report.warnings,
        "infos": report.infos,
    }

    health = ArchitectureHealth(
        score=score,
        grade=_grade(score),
        deductions=deductions,
        metrics=metrics,
    )

    report.health = health
    return health
