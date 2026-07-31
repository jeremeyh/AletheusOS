"""CLI for Kinekt™ Architectural Digital Twin."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import TwinEngine
from .query import query_node


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m aletheus.tooling.kinekt.twin")
    subcommands = parser.add_subparsers(dest="command", required=True)

    build = subcommands.add_parser("build")
    build.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/twin"),
    )
    build.add_argument("--previous", type=Path)

    query = subcommands.add_parser("query")
    query.add_argument("--node", required=True)
    query.add_argument(
        "--snapshot",
        type=Path,
        default=Path(
            "reports/architecture/kinekt/twin/architectural-digital-twin.json"
        ),
    )
    return parser


def _reports() -> dict[str, Path]:
    root = Path("reports/architecture/kinekt")
    return {
        "repository": root / "repository-intelligence.json",
        "topology": root / "topology/runtime-topology.json",
        "dependency": root / "dependency/constitutional-dependency-graph.json",
        "integrity": root / "integrity/platform-integrity.json",
        "cohesion": root / "cohesion/repository-cohesion.json",
        "boundary": root / "boundary/runtime-boundaries.json",
        "health": root / "health/constitutional-health.json",
        "optimization": root / "optimization/optimization-roadmap.json",
        "orchestration": root / "orchestration/execution-manifest.json",
    }


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "query":
        node = query_node(args.snapshot, args.node)
        print(json.dumps(node, indent=2, sort_keys=True))
        return 0 if node is not None else 1

    snapshot = TwinEngine(
        reports=_reports(),
        output=args.output,
        previous=args.previous,
    ).build()
    print(
        "Kinekt twin complete: "
        f"snapshot={snapshot.snapshot_id}, "
        f"nodes={len(snapshot.nodes)}, "
        f"relationships={len(snapshot.relationships)}."
    )
    print(f"Reports: {args.output.resolve()}")
    return 0
