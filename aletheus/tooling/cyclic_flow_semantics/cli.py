from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/cyclic_flow_semantics"),
    )
    args = parser.parse_args()
    report = Engine(
        Path("reports/architecture/kinekt/wiring/constitutional-wiring-manifest.json"),
        args.output,
    ).build()
    print(
        "Cyclic Flow Semantics complete: "
        f"groups={report['cycle_group_count']}, "
        f"unclassified={len(report['unclassified_cycles'])}."
    )
    return 0
