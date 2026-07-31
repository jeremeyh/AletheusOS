"""Command-line interface for Kinekt™ finding resolution."""

from __future__ import annotations

import argparse
from pathlib import Path

from .engine import FindingResolutionEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m aletheus.tooling.kinekt.resolution",
        description="Resolve and prioritize Kinekt repository findings.",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("reports/architecture/kinekt/repository-intelligence.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt"),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = FindingResolutionEngine(args.source, args.output).run()
    counts = report.count_by_tier()
    print(
        "Kinekt resolution complete: "
        f"{len(report.items)} findings; "
        f"{counts.get('critical', 0)} critical, "
        f"{counts.get('high', 0)} high, "
        f"{counts.get('medium', 0)} medium, "
        f"{counts.get('low', 0)} low, "
        f"{counts.get('suppressed', 0)} suppressed."
    )
    print(f"Reports: {args.output.resolve()}")
    return 0
