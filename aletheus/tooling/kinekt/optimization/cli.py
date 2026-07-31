"""CLI for Kinekt™ Optimization Planner."""

from __future__ import annotations

import argparse
from pathlib import Path

from .engine import OptimizationEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m aletheus.tooling.kinekt.optimization"
    )
    parser.add_argument("command", choices=("analyze",), nargs="?", default="analyze")
    parser.add_argument(
        "--resolution-report",
        type=Path,
        default=Path("reports/architecture/kinekt/finding-resolution.json"),
    )
    parser.add_argument(
        "--integrity-report",
        type=Path,
        default=Path("reports/architecture/kinekt/integrity/platform-integrity.json"),
    )
    parser.add_argument(
        "--dependency-report",
        type=Path,
        default=Path(
            "reports/architecture/kinekt/dependency/constitutional-dependency-graph.json"
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
        "--health-report",
        type=Path,
        default=Path("reports/architecture/kinekt/health/constitutional-health.json"),
    )
    parser.add_argument(
        "--output", type=Path, default=Path("reports/architecture/kinekt/optimization")
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    plan = OptimizationEngine(
        args.resolution_report,
        args.integrity_report,
        args.dependency_report,
        args.cohesion_report,
        args.boundary_report,
        args.health_report,
        args.output,
    ).analyze()
    print(
        "Kinekt optimization complete: "
        f"{len(plan.candidates)} candidates, "
        f"{len(plan.work_packages)} work packages, "
        f"{len(plan.quick_wins)} quick wins."
    )
    print(f"Reports: {args.output.resolve()}")
    return 0
