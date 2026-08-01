import asyncio

from aletheus.tooling.runtime_scheduler.engine import RuntimeScheduler
from aletheus.tooling.runtime_scheduler.models import ScheduledTask


def test_scheduler_runs_event_driven_task(tmp_path) -> None:
    scheduler = RuntimeScheduler(tmp_path / "out")

    async def handler(task: ScheduledTask) -> dict[str, object]:
        return {"task_id": task.task_id}

    scheduler.on("mission.submitted", handler)

    async def run() -> dict[str, object]:
        await scheduler.schedule(
            ScheduledTask.immediate("one", "mission.submitted", {})
        )
        return await scheduler.run_until_empty()

    report = asyncio.run(run())
    assert report["task_count"] == 1
    assert report["tasks"][0]["status"] == "completed"
