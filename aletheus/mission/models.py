from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
import uuid


def now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class MissionTask:
    title: str
    description: str = ""
    status: str = "pending"
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    completed_at: str | None = None

    def complete(self) -> None:
        self.status = "completed"
        self.completed_at = now()

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class Mission:
    title: str
    objective: str
    application: str = "system"
    priority: str = "medium"
    status: str = "active"
    tasks: List[MissionTask] = field(default_factory=list)
    mission_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    completed_at: str | None = None

    def complete(self) -> None:
        self.status = "completed"
        self.completed_at = now()

    def progress(self) -> float:
        if not self.tasks:
            return 0.0
        completed = len([task for task in self.tasks if task.status == "completed"])
        return round(completed / len(self.tasks), 2)

    def to_dict(self) -> Dict[str, Any]:
        data = self.__dict__.copy()
        data["tasks"] = [task.to_dict() for task in self.tasks]
        data["progress"] = self.progress()
        return data


@dataclass
class MissionRun:
    mission_id: str
    status: str
    actions: List[Dict[str, Any]]
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
