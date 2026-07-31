from __future__ import annotations

from collections import Counter
from pathlib import Path

from .models import AuditReport

DEFAULT_MAX_MODULE_LINES = 750


def check_runtime_root(report: AuditReport, runtime_root: Path) -> None:
    if not runtime_root.exists():
        report.add_finding(
            "error",
            "runtime_root",
            "Runtime package directory does not exist.",
            str(runtime_root),
        )
    elif not runtime_root.is_dir():
        report.add_finding(
            "error",
            "runtime_root",
            "Runtime package path is not a directory.",
            str(runtime_root),
        )


def check_module_inventory(
    report: AuditReport,
    max_module_lines: int = DEFAULT_MAX_MODULE_LINES,
) -> None:
    """Validate basic module inventory characteristics."""

    if not report.modules:
        report.add_finding(
            "error",
            "module_inventory",
            "No runtime Python modules were discovered.",
        )
        return

    module_names = Counter(module.name for module in report.modules)

    for module in report.modules:
        location = str(module.relative_path)

        if module.size_bytes == 0:
            report.add_finding(
                "warning",
                "empty_module",
                "Python module is empty.",
                location,
                module=module.name,
            )

        if module.lines > max_module_lines:
            report.add_finding(
                "warning",
                "module_size",
                (
                    f"Module contains {module.lines} lines and exceeds the "
                    f"recommended threshold of {max_module_lines}."
                ),
                location,
                module=module.name,
                lines=module.lines,
                threshold=max_module_lines,
            )

    for module_name, count in sorted(module_names.items()):
        if count > 1:
            report.add_finding(
                "error",
                "duplicate_module",
                f"Duplicate runtime module name discovered: {module_name}",
                count=count,
            )


def check_empty_packages(report: AuditReport, runtime_root: Path) -> None:
    """Flag directories that contain no Python modules or child packages."""

    if not runtime_root.exists():
        return

    for directory in sorted(
        path
        for path in runtime_root.rglob("*")
        if path.is_dir() and path.name != "__pycache__"
    ):
        meaningful_entries = [
            child
            for child in directory.iterdir()
            if child.name != "__pycache__" and not child.name.endswith(".pyc")
        ]

        if meaningful_entries:
            continue

        report.add_finding(
            "warning",
            "empty_package",
            "Runtime package directory contains no source files.",
            str(directory.relative_to(runtime_root.parent.parent)),
        )


def run_foundation_checks(
    report: AuditReport,
    runtime_root: Path,
    max_module_lines: int = DEFAULT_MAX_MODULE_LINES,
) -> None:
    check_runtime_root(report, runtime_root)
    check_module_inventory(report, max_module_lines=max_module_lines)
    check_empty_packages(report, runtime_root)
