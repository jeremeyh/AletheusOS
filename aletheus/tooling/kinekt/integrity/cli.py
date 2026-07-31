"""CLI for Kinekt™ Platform Integrity."""

from __future__ import annotations

import argparse
from pathlib import Path

from .engine import IntegrityEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m aletheus.tooling.kinekt.integrity")
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
        "--resolution-report",
        type=Path,
        default=Path("reports/architecture/kinekt/finding-resolution.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/integrity"),
    )
    parser.add_argument("--baseline", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()

    engine = IntegrityEngine(
        repository_report=args.repository_report,
        resolution_report=args.resolution_report,
        output=args.output,
        baseline=args.baseline,
    )
    report = engine.analyze()

    print(
        "Kinekt integrity complete: "
        f"score={report.total_score:.2f}, "
        f"status={report.status}, trend={report.trend}."
    )
    print(f"Reports: {args.output.resolve()}")

    if args.command == "validate" and report.status == "critical":
        return 1
    return 0
