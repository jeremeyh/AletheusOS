from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


def new_execution_id() -> str:
    return f"EXEC-{uuid4().hex[:12].upper()}"


@dataclass(slots=True)
class ExecutionStep:
    name: str
    status: str = "completed"
    detail: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=_timestamp)

    def to_dict(self):
        return {
            "name": self.name,
            "status": self.status,
            "detail": self.detail,
            "timestamp": self.timestamp,
        }


@dataclass(slots=True)
class ExecutionRecord:
    execution_id: str
    identity: str
    application: str
    query: str
    intent: str = ""
    status: str = "created"
    engines: list[str] = field(default_factory=list)
    decision: dict[str, Any] = field(default_factory=dict)
    result: Any = None
    reasoning: list[str] = field(default_factory=list)
    timeline: list[ExecutionStep] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_timestamp)

    def add_step(
        self,
        name: str,
        status: str = "completed",
        detail: dict[str, Any] | None = None,
    ):
        step = ExecutionStep(
            name=name,
            status=status,
            detail=detail or {},
        )
        self.timeline.append(step)
        return step

    def to_dict(self):
        return {
            "execution_id": self.execution_id,
            "identity": self.identity,
            "application": self.application,
            "query": self.query,
            "intent": self.intent,
            "status": self.status,
            "engines": self.engines,
            "decision": self.decision,
            "result": self.result,
            "reasoning": self.reasoning,
            "timeline": [step.to_dict() for step in self.timeline],
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
