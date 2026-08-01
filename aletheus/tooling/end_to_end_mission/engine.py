from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from aletheus.tooling.event_pipeline.engine import EventPipeline
from aletheus.tooling.event_pipeline.models import ConstitutionalEvent
from aletheus.tooling.execution_runtime.engine import ExecutionRuntime
from aletheus.tooling.runtime_scheduler.engine import RuntimeScheduler
from aletheus.tooling.runtime_scheduler.models import ScheduledTask


class MissionExecutionEngine:
    def __init__(
        self,
        process_grid: Path,
        service_bus: Path,
        output: Path,
    ) -> None:
        self.process_grid = process_grid
        self.service_bus = service_bus
        self.output = output

    async def execute(
        self,
        mission_id: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        runtime = ExecutionRuntime(
            self.process_grid,
            self.output / "runtime",
        )
        pipeline = EventPipeline(
            self.service_bus,
            self.output / "events",
        )
        scheduler = RuntimeScheduler(self.output / "scheduler")

        event_trace: list[str] = []

        async def event_recorder(event: ConstitutionalEvent) -> None:
            event_trace.append(event.event_type)

        pipeline.subscribe("*", event_recorder)

        async def mission_handler(task: ScheduledTask) -> dict[str, Any]:
            await pipeline.publish(
                ConstitutionalEvent(
                    event_type="evidence.created",
                    authority="Evidence Engine",
                    payload=task.payload,
                )
            )
            result = await runtime.execute(mission_id, dict(task.payload))
            await pipeline.publish(
                ConstitutionalEvent(
                    event_type="execution.completed",
                    authority="Constitutional Execution Runtime",
                    payload={"status": result.status},
                )
            )
            await pipeline.publish(
                ConstitutionalEvent(
                    event_type="platform.certified",
                    authority="Platform Certification",
                    payload={
                        "status": "ready" if result.status == "completed" else "blocked"
                    },
                )
            )
            return result.to_dict()

        scheduler.on("mission.submitted", mission_handler)
        await scheduler.schedule(
            ScheduledTask.immediate(
                mission_id,
                "mission.submitted",
                payload or {},
            )
        )
        scheduler_report = await scheduler.run_until_empty()
        task_result = scheduler_report["tasks"][0]
        mission_result = task_result.get("results", [{}])[0]
        status = mission_result.get("status", "failed")

        report = {
            "mission_id": mission_id,
            "status": status,
            "event_trace": event_trace,
            "scheduler": scheduler_report,
            "platform_certification": "READY" if status == "completed" else "BLOCK",
            "path": [
                "Evidence Engine",
                "Knowledge Resolution",
                "Reasoning",
                "Planning",
                "Decision",
                "Execution",
                "Platform Certification",
            ],
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "end-to-end-mission-execution.json").write_text(
            json.dumps(report, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return report
