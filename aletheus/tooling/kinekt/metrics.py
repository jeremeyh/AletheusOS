"""Package health metrics."""

from __future__ import annotations

from collections import Counter, defaultdict

from .graph import RepositoryGraph
from .models import Finding, ModuleRecord, PackageMetric


def calculate_package_metrics(
    modules: list[ModuleRecord],
    graph: RepositoryGraph,
    findings: list[Finding],
) -> list[PackageMetric]:
    by_package: dict[str, list[ModuleRecord]] = defaultdict(list)
    for module in modules:
        by_package[module.package].append(module)

    orphan_counts: Counter[str] = Counter()
    duplicate_counts: Counter[str] = Counter()
    boundary_counts: Counter[str] = Counter()
    module_to_package = {module.module: module.package for module in modules}

    for finding in findings:
        package = module_to_package.get(finding.subject)
        if package is None:
            package = ".".join(finding.subject.split(".")[:2])

        if finding.code == "ORPHAN_CANDIDATE":
            orphan_counts[package] += 1
        elif finding.code == "EXACT_STRUCTURAL_DUPLICATE":
            duplicate_counts[package] += 1
        elif finding.code == "BOUNDARY_VIOLATION":
            boundary_counts[package] += 1

    metrics: list[PackageMetric] = []
    for package, package_modules in sorted(by_package.items()):
        names = {module.module for module in package_modules}
        orphans = orphan_counts[package]
        duplicates = duplicate_counts[package]
        boundaries = boundary_counts[package]
        deduction = min(100, orphans * 2 + duplicates * 4 + boundaries * 10)

        metrics.append(
            PackageMetric(
                package=package,
                modules=len(package_modules),
                definitions=sum(len(module.definitions) for module in package_modules),
                lines=sum(module.lines for module in package_modules),
                internal_fan_in=sum(graph.fan_in(name) for name in names),
                internal_fan_out=sum(graph.fan_out(name) for name in names),
                orphan_candidates=orphans,
                duplicate_definitions=duplicates,
                boundary_findings=boundaries,
                health_score=max(0, 100 - deduction),
            )
        )

    return metrics
