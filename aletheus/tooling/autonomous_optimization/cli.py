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
        default=Path("reports/architecture/kinekt/autonomous_optimization"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "runtime_diagnostics/constitutional-runtime-diagnostics.json",
        root / "optimization/optimization-roadmap.json",
        args.output,
    ).build()
    print(
        "Autonomous Runtime Optimization complete: "
        f"proposals={report['proposal_count']}, mode={report['mode']}."
    )
    return 0
