from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from .engine import MissionExecutionEngine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("execute",), nargs="?", default="execute")
    parser.add_argument("--mission-id", default="genesis-19.6-smoke")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/end_to_end_mission"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    engine = MissionExecutionEngine(
        root / "process_composer/constitutional-process-composition.json",
        root / "runtime_service_bus/runtime-service-bus.json",
        args.output,
    )
    report = asyncio.run(
        engine.execute(
            args.mission_id,
            {"source": "cli", "purpose": "end-to-end-smoke"},
        )
    )
    print(
        "End-to-End Mission Execution complete: "
        f"mission={report['mission_id']}, "
        f"status={report['status']}, "
        f"certification={report['platform_certification']}."
    )
    return 0 if report["status"] == "completed" else 1
