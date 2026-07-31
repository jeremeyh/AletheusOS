"""Architectural analyzers."""

from __future__ import annotations

from collections import defaultdict

from .configuration import BoundaryRule
from .graph import RepositoryGraph
from .models import Finding, ModuleRecord


def duplicate_findings(modules: list[ModuleRecord]) -> list[Finding]:
    grouped: dict[str, list] = defaultdict(list)
    for module in modules:
        for definition in module.definitions:
            grouped[definition.fingerprint].append(definition)

    findings: list[Finding] = []
    for records in grouped.values():
        if len({record.path for record in records}) < 2:
            continue
        subjects = tuple(sorted(record.qualified_name for record in records))
        findings.append(
            Finding(
                code="EXACT_STRUCTURAL_DUPLICATE",
                severity="warning",
                subject=subjects[0],
                message="Exact AST-equivalent definitions exist in multiple files.",
                evidence=subjects,
            )
        )
    return findings


def orphan_findings(
    modules: list[ModuleRecord],
    graph: RepositoryGraph,
) -> list[Finding]:
    findings: list[Finding] = []
    for module in modules:
        if module.path.endswith("__init__.py"):
            continue
        if module.module.startswith("tests.") or ".tests." in module.module:
            continue
        if graph.fan_in(module.module) != 0 or not module.definitions:
            continue

        findings.append(
            Finding(
                code="ORPHAN_CANDIDATE",
                severity="advisory",
                subject=module.module,
                message=(
                    "No internal module imports this definition-bearing module. "
                    "Dynamic registration or external use may still exist."
                ),
                evidence=(module.path,),
            )
        )
    return findings


def boundary_findings(
    modules: list[ModuleRecord],
    rules: tuple[BoundaryRule, ...],
) -> list[Finding]:
    findings: list[Finding] = []
    for module in modules:
        for imported in module.imports:
            for rule in rules:
                if module.module.startswith(rule.source_prefix) and imported.startswith(
                    rule.forbidden_target_prefix
                ):
                    findings.append(
                        Finding(
                            code="BOUNDARY_VIOLATION",
                            severity="error",
                            subject=module.module,
                            message=rule.reason,
                            evidence=(module.path, imported),
                        )
                    )
    return findings


def syntax_findings(modules: list[ModuleRecord]) -> list[Finding]:
    return [
        Finding(
            code="SYNTAX_ERROR",
            severity="error",
            subject=module.module,
            message="Module could not be parsed by the active Python interpreter.",
            evidence=(module.path,),
        )
        for module in modules
        if not module.syntax_valid
    ]
