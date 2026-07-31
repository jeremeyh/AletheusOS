from __future__ import annotations

from pathlib import Path

from .boot_analysis import analyze_boot_pipeline
from .checks import (
    check_empty_packages,
    check_module_inventory,
    check_runtime_root,
)
from .dependency_graph import write_dependency_graph_reports
from .discovery import discover_runtime_modules
from .health import calculate_health
from .imports import analyze_imports
from .kernel_analysis import analyze_kernel_construction
from .legacy_analysis import analyze_legacy_references
from .models import AuditReport
from .parser import parse_runtime_modules
from .reporting import write_reports


def run_runtime_architecture_audit(
    repo_root: Path,
    runtime_root: Path,
    report_root: Path,
    max_module_lines: int = 750,
) -> AuditReport:
    """Run the complete runtime architecture audit."""

    report = AuditReport()

    check_runtime_root(report, runtime_root)

    report.modules = discover_runtime_modules(runtime_root)

    check_module_inventory(
        report,
        max_module_lines=max_module_lines,
    )
    check_empty_packages(report, runtime_root)

    report.parsed_modules = parse_runtime_modules(
        report.modules,
        report,
    )

    graph = analyze_imports(report)

    analyze_kernel_construction(report)
    analyze_boot_pipeline(report)
    analyze_legacy_references(report)

    calculate_health(report)

    write_reports(
        report=report,
        repo_root=repo_root,
        runtime_root=runtime_root,
        output_root=report_root,
    )

    write_dependency_graph_reports(
        graph=graph,
        cycles=report.dependency_cycles,
        output_root=report_root,
    )

    return report
