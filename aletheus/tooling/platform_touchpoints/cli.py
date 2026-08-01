from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output", type=Path, default=Path("reports/architecture/kinekt/touchpoints")
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "access_modules/access-module-realization.json",
        root / "knowledge_graph/runtime-knowledge-graph.json",
        args.output,
    ).build()
    print(
        f"Platform Touchpoint Matrix complete: touchpoints={report['touchpoint_count']}."
    )
    return 0
