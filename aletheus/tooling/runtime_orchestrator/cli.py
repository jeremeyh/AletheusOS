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
        default=Path("reports/architecture/kinekt/runtime_orchestrator"),
    )
    args = parser.parse_args()
    report = Engine(
        Path(
            "reports/architecture/kinekt/execution_plan/constitutional-execution-plan.json"
        ),
        args.output,
    ).build()
    print(f"Runtime Orchestrator complete: units={report['unit_count']}.")
    return 0
