"""CLI for Kinekt™ Runtime Topology."""

from __future__ import annotations

import argparse
from pathlib import Path

from .engine import TopologyEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m aletheus.tooling.kinekt.topology")
    parser.add_argument(
        "command",
        choices=("analyze",),
        nargs="?",
        default="analyze",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("reports/architecture/kinekt/repository-intelligence.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/topology"),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = TopologyEngine(args.source, args.output).analyze()

    print(
        "Kinekt topology complete: "
        f"{len(report.modules)} modules, "
        f"{len(report.cycles)} cycle groups, "
        f"{len(report.isolated)} isolated modules."
    )
    print(f"Reports: {args.output.resolve()}")
    return 0
