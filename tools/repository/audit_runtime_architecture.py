#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from runtime_architecture_audit.runner import (
    run_runtime_architecture_audit,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RUNTIME_ROOT = REPO_ROOT / "aletheus" / "runtime"
DEFAULT_REPORT_ROOT = REPO_ROOT / "reports" / "architecture"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the AletheusOS runtime architecture using Python AST "
            "analysis and generate Markdown, JSON, and dependency-graph "
            "reports."
        )
    )

    parser.add_argument(
        "--runtime-root",
        type=Path,
        default=DEFAULT_RUNTIME_ROOT,
        help="Runtime package directory to analyze.",
    )

    parser.add_argument(
        "--report-root",
        type=Path,
        default=DEFAULT_REPORT_ROOT,
        help="Directory where audit reports will be written.",
    )

    parser.add_argument(
        "--max-module-lines",
        type=int,
        default=750,
        help="Recommended maximum Python module length.",
    )

    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Return a nonzero status when warnings are discovered.",
    )

    return parser


def main() -> int:
    args = build_parser().parse_args()

    report = run_runtime_architecture_audit(
        repo_root=REPO_ROOT,
        runtime_root=args.runtime_root.resolve(),
        report_root=args.report_root.resolve(),
        max_module_lines=args.max_module_lines,
    )

    print(
        "Runtime architecture audit complete: "
        f"{len(report.modules)} modules, "
        f"{report.errors} errors, "
        f"{report.warnings} warnings, "
        f"health {report.health.score}/100 "
        f"({report.health.grade})."
    )

    print(
        "Reports:"
        f"\n  {args.report_root / 'runtime-architecture-audit.md'}"
        f"\n  {args.report_root / 'runtime-architecture-audit.json'}"
        f"\n  {args.report_root / 'runtime-dependency-graph.md'}"
        f"\n  {args.report_root / 'runtime-dependency-graph.json'}"
    )

    if report.errors:
        return 1

    if args.fail_on_warning and report.warnings:
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
