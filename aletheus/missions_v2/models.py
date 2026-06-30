from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
import uuid


def now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class MissionTaskV2:
    title: str
    description: str = ""
    assigned_agent: str = "Executive Agent"
    application: str = "AletheusOS"
    status: str = "queued"
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    started_at: str | None = None
    completed_at: str | None = None
    result: Dict[str, Any] = field(default_factory=dict)

    def start(self) -> None:
        self.status = "running"
        self.started_at = now()

    def complete(self, result: Dict[str, Any] | None = None) -> None:
        self.status = "completed"
        self.completed_at = now()
        self.result = result or {}

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class AutonomousMissionV2:
    title: str
    objective: str
    application: str = "AletheusOS"
    priority: str = "high"
    status: str = "created"
    tasks: List[MissionTaskV2] = field(default_factory=list)
    mission_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    started_at: str | None = None
    completed_at: str | None = None

    def progress(self) -> float:
        if not self.tasks:
            return 0.0
        completed = len([task for task in self.tasks if task.status == "completed"])
        return round(completed / len(self.tasks), 2)

    def start(self) -> None:
        self.status = "running"
        self.started_at = now()

    def complete_if_ready(self) -> None:
        if self.tasks and all(task.status == "completed" for task in self.tasks):
            self.status = "completed"
            self.completed_at = now()

    def to_dict(self) -> Dict[str, Any]:
        data = self.__dict__.copy()
        data["tasks"] = [task.to_dict() for task in self.tasks]
        data["progress"] = self.progress()
        return data


@dataclass
class MissionTelemetryV2:
    mission_id: str
    event_type: str
    message: str
    payload: Dict[str, Any] = field(default_factory=dict)
    telemetry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
