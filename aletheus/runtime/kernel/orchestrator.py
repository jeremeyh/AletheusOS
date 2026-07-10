from __future__ import annotations

from aletheus.time_utils import utc_now, utc_now_iso

from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Any, Dict, List
import uuid


def utc_now() -> str:
    return utc_now_iso()


@dataclass
class IntelligenceTask:
    task_id: str
    command: str
    payload: Dict[str, Any]
    status: str = "queued"
    priority: int = 5
    result: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    started_at: str | None = None
    completed_at: str | None = None
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)


class IntelligenceOrchestrator:
    VERSION = "4.0.0"

    def __init__(self) -> None:
        self.tasks: Dict[str, IntelligenceTask] = {}
        self.history: List[Dict[str, Any]] = []

    @property
    def version(self):
        return self.VERSION

    def create_task(
        self,
        command: str,
        payload: Dict[str, Any] | None = None,
        priority: int = 5,
        metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        task = IntelligenceTask(
            task_id=str(uuid.uuid4()),
            command=command,
            payload=payload or {},
            priority=priority,
            metadata=metadata or {},
        )

        self.tasks[task.task_id] = task
        self.history.append(
            {
                "event": "task.created",
                "task_id": task.task_id,
                "command": command,
                "timestamp": utc_now(),
            }
        )

        return asdict(task)

    def execute_task(self, task_id: str, runtime: Any) -> Dict[str, Any]:
        task = self.tasks.get(task_id)

        if task is None:
            return {"error": "Task not found"}

        task.status = "running"
        task.started_at = utc_now()

        try:
            # Dispatch directly through the runtime command bus.
            # Avoid routing back through the kernel executor.
            context = runtime.commands.dispatch(
                task.command,
                task.payload,
            )

            task.result = dict(context.results)
            task.errors = list(context.errors)

            if context.errors:
                task.status = "failed"
            else:
                task.status = "completed"

        except Exception as exc:
            task.status = "failed"
            task.errors.append(str(exc))

        task.completed_at = utc_now()

        self.history.append(
            {
                "event": "task.completed",
                "task_id": task.task_id,
                "status": task.status,
                "timestamp": utc_now(),
            }
        )

        return asdict(task)

    def execute(
        self,
        command: str,
        payload: Dict[str, Any] | None,
        runtime: Any,
        priority: int = 5,
    ) -> Dict[str, Any]:
        task = self.create_task(
            command=command,
            payload=payload or {},
            priority=priority,
        )

        return self.execute_task(task["task_id"], runtime)

    def list_tasks(self) -> Dict[str, Any]:
        return {
            "tasks": [
                asdict(task)
                for task in self.tasks.values()
            ]
        }

    def statistics(self) -> Dict[str, Any]:
        return {
            "version": self.VERSION,
            "tasks": len(self.tasks),
            "queued": sum(1 for t in self.tasks.values() if t.status == "queued"),
            "running": sum(1 for t in self.tasks.values() if t.status == "running"),
            "completed": sum(1 for t in self.tasks.values() if t.status == "completed"),
            "failed": sum(1 for t in self.tasks.values() if t.status == "failed"),
            "history_events": len(self.history),
            "health": "healthy",
        }


intelligence_orchestrator = IntelligenceOrchestrator()
