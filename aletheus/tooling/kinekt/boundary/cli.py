"""CLI for Kinekt™ Runtime Boundary Analyzer."""

from __future__ import annotations

import argparse
from pathlib import Path

from .engine import BoundaryEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m aletheus.tooling.kinekt.boundary")
    parser.add_argument(
        "command",
        choices=("analyze", "validate"),
        nargs="?",
        default="analyze",
    )
    parser.add_argument(
        "--dependency-report",
        type=Path,
        default=Path(
            "reports/architecture/kinekt/dependency/"
            "constitutional-dependency-graph.json"
        ),
    )
    parser.add_argument(
        "--cohesion-report",
        type=Path,
        default=Path("reports/architecture/kinekt/cohesion/repository-cohesion.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/boundary"),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = BoundaryEngine(
        args.dependency_report,
        args.cohesion_report,
        args.output,
    ).analyze()

    high = sum(finding.severity == "high" for finding in report.findings)
    print(
        "Kinekt boundary analysis complete: "
        f"{len(report.findings)} findings, "
        f"{high} high, "
        f"{report.unresolved_relationships} unresolved relationships."
    )
    print(f"Reports: {args.output.resolve()}")

    if args.command == "validate" and high:
        return 1
    return 0
