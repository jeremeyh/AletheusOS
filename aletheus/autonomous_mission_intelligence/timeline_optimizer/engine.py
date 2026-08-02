from __future__ import annotations

from typing import Any, ClassVar

from .helpers import digest
from .models import TimelineTask


class Engine:
    VERSION: ClassVar[str] = "34.14.0"

    def optimize(self, tasks: list[TimelineTask]) -> dict[str, Any]:
        task_map = {task.task_id: task for task in tasks}
        schedule: dict[str, dict[str, float]] = {}
        unresolved = set(task_map)
        while unresolved:
            progress = False
            for task_id in sorted(unresolved):
                task = task_map[task_id]
                if all(dep in schedule for dep in task.dependencies):
                    dependency_end = max(
                        (schedule[dep]["end"] for dep in task.dependencies), default=0.0
                    )
                    start = max(task.earliest_start, dependency_end)
                    end = start + max(task.duration, 0.0)
                    schedule[task_id] = {"start": round(start, 6), "end": round(end, 6)}
                    unresolved.remove(task_id)
                    progress = True
                    break
            if not progress:
                break
        deadline_misses = [
            task_id
            for task_id, slot in schedule.items()
            if task_map[task_id].deadline is not None
            and slot["end"] > task_map[task_id].deadline
        ]
        payload = {
            "schedule": schedule,
            "unresolved": sorted(unresolved),
            "deadlineMisses": sorted(deadline_misses),
            "valid": not unresolved,
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(self, tasks: list[TimelineTask]) -> dict[str, Any]:
        return self.optimize(tasks)
