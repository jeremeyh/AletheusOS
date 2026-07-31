"""CLI for Kinekt™ Evolution Orchestrator."""

from __future__ import annotations

import argparse
from pathlib import Path

from .engine import OrchestrationEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m aletheus.tooling.kinekt.orchestration"
    )
    parser.add_argument(
        "command",
        choices=("plan", "validate"),
        nargs="?",
        default="plan",
    )
    parser.add_argument(
        "--roadmap",
        type=Path,
        default=Path(
            "reports/architecture/kinekt/optimization/optimization-roadmap.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/orchestration"),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest = OrchestrationEngine(args.roadmap, args.output).plan()

    print(
        "Kinekt orchestration complete: "
        f"{len(manifest.units)} execution units, "
        f"{len(manifest.abstentions)} abstentions, "
        f"status={manifest.status}."
    )
    print(f"Reports: {args.output.resolve()}")

    if args.command == "validate" and manifest.status != "planned":
        return 1
    return 0
