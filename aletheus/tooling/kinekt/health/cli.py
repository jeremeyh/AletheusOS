"""CLI for Kinekt™ Constitutional Health."""

from __future__ import annotations

import argparse
from pathlib import Path

from .engine import HealthEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m aletheus.tooling.kinekt.health")
    parser.add_argument(
        "command",
        choices=("analyze", "validate"),
        nargs="?",
        default="analyze",
    )
    parser.add_argument(
        "--integrity-report",
        type=Path,
        default=Path("reports/architecture/kinekt/integrity/platform-integrity.json"),
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
        "--cohesion-report",
        type=Path,
        default=Path("reports/architecture/kinekt/cohesion/repository-cohesion.json"),
    )
    parser.add_argument(
        "--boundary-report",
        type=Path,
        default=Path("reports/architecture/kinekt/boundary/runtime-boundaries.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/health"),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = HealthEngine(
        args.integrity_report,
        args.topology_report,
        args.dependency_report,
        args.cohesion_report,
        args.boundary_report,
        args.output,
    ).analyze()

    print(
        "Kinekt constitutional health complete: "
        f"score={report.total_score:.2f}, "
        f"status={report.status}, "
        f"readiness={report.readiness}."
    )
    print(f"Reports: {args.output.resolve()}")

    if args.command == "validate" and report.readiness == "not_ready":
        return 1
    return 0
