from __future__ import annotations

import asyncio
import json
from collections import defaultdict
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

from .models import ScheduledTask

TaskHandler = Callable[[ScheduledTask], Awaitable[dict[str, Any]]]


class RuntimeScheduler:
    def __init__(self, output: Path) -> None:
        self.output = output
        self._queue: asyncio.PriorityQueue[tuple[str, str, ScheduledTask]] = (
            asyncio.PriorityQueue()
        )
        self._handlers: dict[str, list[TaskHandler]] = defaultdict(list)

    def on(self, trigger: str, handler: TaskHandler) -> None:
        self._handlers[trigger].append(handler)

    async def schedule(self, task: ScheduledTask) -> None:
        await self._queue.put((task.due_at, task.task_id, task))

    async def run_until_empty(self) -> dict[str, Any]:
        results = []
        while not self._queue.empty():
            _due_at, _task_id, task = await self._queue.get()
            handlers = self._handlers.get(task.trigger, [])
            if not handlers:
                results.append(
                    {
                        "task_id": task.task_id,
                        "status": "unhandled",
                        "trigger": task.trigger,
                    }
                )
                continue
            handler_results = await asyncio.gather(
                *(handler(task) for handler in handlers)
            )
            results.append(
                {
                    "task_id": task.task_id,
                    "status": "completed",
                    "trigger": task.trigger,
                    "results": handler_results,
                }
            )
        report = {"tasks": results, "task_count": len(results)}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "runtime-scheduler-integration.json").write_text(
            json.dumps(report, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return report
