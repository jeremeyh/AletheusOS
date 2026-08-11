from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class WorkflowNode:
    title: str
    node_type: str = "agent"
    command: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    assigned_agent: str = "Executive Agent"
    application: str = "AletheusOS"
    status: str = "queued"
    result: dict[str, Any] = field(default_factory=dict)
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    started_at: str | None = None
    completed_at: str | None = None

    def start(self) -> None:
        self.status = "running"
        self.started_at = now()

    def complete(self, result: dict[str, Any] | None = None) -> None:
        self.status = "completed"
        self.completed_at = now()
        self.result = result or {}

    def fail(self, result: dict[str, Any] | None = None) -> None:
        self.status = "failed"
        self.completed_at = now()
        self.result = result or {}

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class WorkflowExecution:
    title: str
    objective: str
    application: str = "AletheusOS"
    status: str = "created"
    nodes: list[WorkflowNode] = field(default_factory=list)
    workflow_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    started_at: str | None = None
    completed_at: str | None = None

    def start(self) -> None:
        self.status = "running"
        self.started_at = now()

    def progress(self) -> float:
        if not self.nodes:
            return 0.0
        completed = len([node for node in self.nodes if node.status == "completed"])
        return round(completed / len(self.nodes), 2)

    def complete_if_ready(self) -> None:
        if self.nodes and all(node.status == "completed" for node in self.nodes):
            self.status = "completed"
            self.completed_at = now()

    def fail_if_needed(self) -> None:
        if any(node.status == "failed" for node in self.nodes):
            self.status = "failed"
            self.completed_at = now()

    def to_dict(self) -> dict[str, Any]:
        data = self.__dict__.copy()
        data["nodes"] = [node.to_dict() for node in self.nodes]
        data["progress"] = self.progress()
        return data


@dataclass
class WorkflowEvent:
    workflow_id: str
    event_type: str
    message: str
    payload: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
