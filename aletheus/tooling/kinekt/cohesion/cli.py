"""CLI for Kinekt™ Repository Cohesion."""

from __future__ import annotations

import argparse
from pathlib import Path

from .engine import CohesionEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m aletheus.tooling.kinekt.cohesion")
    parser.add_argument(
        "command",
        choices=("analyze", "validate"),
        nargs="?",
        default="analyze",
    )
    parser.add_argument(
        "--topology-report",
        type=Path,
        default=Path("reports/architecture/kinekt/topology/runtime-topology.json"),
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
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/cohesion"),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = CohesionEngine(
        args.topology_report,
        args.dependency_report,
        args.output,
    ).analyze()

    print(
        "Kinekt cohesion complete: "
        f"score={report.average_score:.2f}, "
        f"status={report.status}, "
        f"hotspots={len(report.hotspots)}."
    )
    print(f"Reports: {args.output.resolve()}")

    if args.command == "validate" and report.status == "critical":
        return 1
    return 0
