from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from aletheus.time_utils import utc_now_iso


def now() -> str:
    return utc_now_iso()


@dataclass
class PlanningStep:
    title: str
    description: str = ""
    assigned_agent: str = "Executive Agent"
    status: str = "pending"
    step_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    completed_at: str | None = None

    def complete(self) -> None:
        self.status = "completed"
        self.completed_at = now()

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class AutonomousPlan:
    objective: str
    strategy: str
    priority: str = "high"
    status: str = "active"
    steps: list[PlanningStep] = field(default_factory=list)
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    completed_at: str | None = None

    def progress(self) -> float:
        if not self.steps:
            return 0.0
        completed = len([step for step in self.steps if step.status == "completed"])
        return round(completed / len(self.steps), 2)

    def complete_if_finished(self) -> None:
        if self.steps and all(step.status == "completed" for step in self.steps):
            self.status = "completed"
            self.completed_at = now()

    def to_dict(self) -> dict[str, Any]:
        data = self.__dict__.copy()
        data["steps"] = [step.to_dict() for step in self.steps]
        data["progress"] = self.progress()
        return data
