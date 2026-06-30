from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
import uuid


def now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class AgentCapability:
    name: str
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class AgentTask:
    title: str
    payload: Dict[str, Any] = field(default_factory=dict)
    status: str = "queued"
    result: Dict[str, Any] = field(default_factory=dict)
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    completed_at: str | None = None

    def complete(self, result: Dict[str, Any]) -> None:
        self.status = "completed"
        self.result = result
        self.completed_at = now()

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class AletheusAgent:
    name: str
    role: str
    description: str = ""
    status: str = "online"
    capabilities: List[AgentCapability] = field(default_factory=list)
    tasks: List[AgentTask] = field(default_factory=list)
    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def assign_task(self, title: str, payload: Dict[str, Any] | None = None) -> AgentTask:
        task = AgentTask(title=title, payload=payload or {})
        self.tasks.append(task)
        return task

    def complete_next_task(self) -> AgentTask | None:
        pending = [task for task in self.tasks if task.status == "queued"]
        if not pending:
            return None

        task = pending[0]
        task.complete(
            {
                "agent": self.name,
                "role": self.role,
                "message": f"{self.name} completed task: {task.title}",
            }
        )
        return task

    def to_dict(self) -> Dict[str, Any]:
        data = self.__dict__.copy()
        data["capabilities"] = [item.to_dict() for item in self.capabilities]
        data["tasks"] = [item.to_dict() for item in self.tasks]
        return data
