from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from .engine import RuntimeScheduler
from .models import ScheduledTask


async def run(output: Path) -> dict[str, object]:
    scheduler = RuntimeScheduler(output)

    async def handler(task: ScheduledTask) -> dict[str, object]:
        return {"accepted": True, "payload": task.payload}

    scheduler.on("mission.submitted", handler)
    await scheduler.schedule(
        ScheduledTask.immediate(
            "genesis-19.5-smoke",
            "mission.submitted",
            {"source": "cli"},
        )
    )
    return await scheduler.run_until_empty()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("run",), nargs="?", default="run")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/runtime_scheduler"),
    )
    args = parser.parse_args()
    report = asyncio.run(run(args.output))
    print(f"Runtime Scheduler Integration complete: tasks={report['task_count']}.")
    return 0
