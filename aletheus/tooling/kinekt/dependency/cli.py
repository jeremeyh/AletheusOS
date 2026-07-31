"""CLI for Kinekt™ Constitutional Dependency Graph."""

from __future__ import annotations

import argparse
from pathlib import Path

from .engine import DependencyEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m aletheus.tooling.kinekt.dependency"
    )
    parser.add_argument(
        "command",
        choices=("analyze", "validate"),
        nargs="?",
        default="analyze",
    )
    parser.add_argument(
        "--repository-report",
        type=Path,
        default=Path("reports/architecture/kinekt/repository-intelligence.json"),
    )
    parser.add_argument(
        "--topology-report",
        type=Path,
        default=Path("reports/architecture/kinekt/topology/runtime-topology.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/dependency"),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = DependencyEngine(
        args.repository_report,
        args.topology_report,
        args.output,
    ).analyze()

    print(
        "Kinekt dependency graph complete: "
        f"{len(report.nodes)} nodes, "
        f"{len(report.relationships)} relationships, "
        f"{len(report.findings)} policy findings, "
        f"{len(report.unresolved_modules)} unresolved modules."
    )
    print(f"Reports: {args.output.resolve()}")

    if args.command == "validate" and any(
        finding.severity == "high" for finding in report.findings
    ):
        return 1
    return 0
