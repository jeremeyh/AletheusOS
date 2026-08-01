from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

from .models import ExecutionContext, ExecutionResult, ProcessStep

StepHandler = Callable[[ExecutionContext, ProcessStep], Awaitable[dict[str, Any]]]


async def default_handler(
    context: ExecutionContext,
    step: ProcessStep,
) -> dict[str, Any]:
    await asyncio.sleep(0)
    event = {
        "step_id": step.step_id,
        "stage": step.stage,
        "status": "completed",
    }
    context.trace.append(event)
    return event


class ExecutionRuntime:
    def __init__(
        self,
        process_grid: Path,
        output: Path,
        handlers: dict[str, StepHandler] | None = None,
    ) -> None:
        self.process_grid = process_grid
        self.output = output
        self.handlers = handlers or {}

    async def execute(
        self,
        mission_id: str,
        payload: dict[str, Any] | None = None,
    ) -> ExecutionResult:
        grid = json.loads(self.process_grid.read_text(encoding="utf-8"))
        context = ExecutionContext(mission_id=mission_id, payload=payload or {})
        results: list[dict[str, Any]] = []

        for item in grid.get("steps", []):
            if not isinstance(item, dict):
                continue
            step = ProcessStep(
                step_id=str(item.get("step_id")),
                stage=str(item.get("stage")),
                validator_id=item.get("validator_id"),
            )
            handler = self.handlers.get(step.stage, default_handler)
            try:
                result = await handler(context, step)
            except (RuntimeError, ValueError, TypeError, LookupError, OSError) as exc:
                failed = {
                    "step_id": step.step_id,
                    "stage": step.stage,
                    "status": "failed",
                    "error": type(exc).__name__,
                }
                results.append(failed)
                return ExecutionResult(
                    mission_id=mission_id,
                    status="failed",
                    steps=results,
                    context={
                        "payload": context.payload,
                        "evidence": context.evidence,
                        "trace": context.trace,
                    },
                )
            results.append(result)

        return ExecutionResult(
            mission_id=mission_id,
            status="completed",
            steps=results,
            context={
                "payload": context.payload,
                "evidence": context.evidence,
                "trace": context.trace,
            },
        )

    def execute_sync(
        self,
        mission_id: str,
        payload: dict[str, Any] | None = None,
    ) -> ExecutionResult:
        return asyncio.run(self.execute(mission_id, payload))

    def write_result(self, result: ExecutionResult) -> Path:
        self.output.mkdir(parents=True, exist_ok=True)
        path = self.output / "constitutional-execution-result.json"
        path.write_text(
            json.dumps(result.to_dict(), indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return path
