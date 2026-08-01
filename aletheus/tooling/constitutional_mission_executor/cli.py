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
        default=Path("reports/architecture/kinekt/constitutional_mission_executor"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "runtime_orchestrator/runtime-orchestration.json",
        root / "mission_execution_graph/mission-execution-graph.json",
        root / "runtime_service_bus/runtime-service-bus.json",
        args.output,
    ).build()
    print(
        "Constitutional Mission Executor complete: "
        f"missions={report['mission_count']}, mode={report['mode']}."
    )
    return 0
