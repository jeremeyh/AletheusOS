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
        default=Path("reports/architecture/kinekt/execution_plan"),
    )
    args = parser.parse_args()
    report = Engine(
        Path("reports/architecture/kinekt/runtime_flows/runtime-flows.json"),
        args.output,
    ).build()
    print(f"Execution Planner complete: steps={report['step_count']}.")
    return 0
