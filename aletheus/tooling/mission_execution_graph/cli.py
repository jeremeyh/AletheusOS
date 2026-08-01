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
        default=Path("reports/architecture/kinekt/mission_execution_graph"),
    )
    args = parser.parse_args()
    report = Engine(
        Path(
            "reports/architecture/kinekt/runtime_orchestrator/runtime-orchestration.json"
        ),
        args.output,
    ).build()
    print(
        "Mission Execution Graph complete: "
        f"nodes={len(report['nodes'])}, edges={len(report['edges'])}."
    )
    return 0
