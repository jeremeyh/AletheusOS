"""CLI for Kinekt™ Repository Evolution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import EvolutionEngine
from .rollback import rollback_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m aletheus.tooling.kinekt.evolution")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/evolution"),
    )

    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("template")

    validate = subcommands.add_parser("validate")
    validate.add_argument("--plan", type=Path, required=True)

    apply_command = subcommands.add_parser("apply")
    apply_command.add_argument("--plan", type=Path, required=True)
    apply_command.add_argument("--approve", action="store_true")

    rollback = subcommands.add_parser("rollback")
    rollback.add_argument("--manifest", type=Path, required=True)

    return parser


def _template() -> dict:
    return {
        "plan_id": "example-plan",
        "summary": "Describe the governed architectural change",
        "operations": [
            {
                "operation": "replace_text",
                "path": "aletheus/example.py",
                "expected_sha256": "<sha256>",
                "old": "old text",
                "new": "new text",
            }
        ],
        "validation": {
            "ruff_targets": ["aletheus/example.py"],
            "compile_targets": ["aletheus/example.py"],
            "pytest_targets": ["tests/example"],
        },
    }


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "template":
        print(json.dumps(_template(), indent=2))
        return 0

    if args.command == "rollback":
        restored = rollback_manifest(args.manifest)
        print(f"Rollback complete: {len(restored)} path(s) restored.")
        return 0

    engine = EvolutionEngine(args.root, args.output)

    if args.command == "validate":
        result = engine.validate(args.plan)
    else:
        result = engine.apply(args.plan, approved=args.approve)

    print(
        f"Evolution {result.mode} complete: "
        f"plan={result.plan_id}, status={result.status}."
    )
    return 0 if result.status in {"validated", "applied"} else 1
