from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", choices=("build", "validate"), nargs="?", default="build"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/semantic_rail_gate"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "root_domain_resolution/explicit-root-domain-resolution.json",
        root / "parallel_rails/parallel-rail-coordination.json",
        root / "forked_authority/forked-authority-resolution.json",
        root / "platform_continuity/full-platform-continuity-gate.json",
        args.output,
    ).build()
    print(f"Semantic Rail Continuity Gate complete: decision={report['decision']}.")
    if args.command == "validate" and report["decision"] == "block":
        return 1
    return 0
