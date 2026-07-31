"""Command-line interface for Kinekt™."""

from __future__ import annotations

import argparse
from pathlib import Path

from .configuration import KinektConfiguration
from .engine import KinektEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m aletheus.tooling.kinekt",
        description="AletheusOS repository intelligence and architecture mapping.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    analyze = subcommands.add_parser("analyze")
    analyze.add_argument("--root", type=Path, default=Path("."))
    analyze.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt"),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    configuration = KinektConfiguration(root=args.root, output=args.output)
    result = KinektEngine(configuration).analyze()
    print(
        "Kinekt analysis complete: "
        f"{len(result.modules)} modules, "
        f"{result.definition_count} definitions, "
        f"{len(result.findings)} findings."
    )
    print(f"Reports: {configuration.output.resolve()}")
    return 0
