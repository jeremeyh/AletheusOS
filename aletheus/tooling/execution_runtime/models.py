from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ProcessStep:
    step_id: str
    stage: str
    validator_id: str | None
    status: str = "pending"


@dataclass(slots=True)
class ExecutionContext:
    mission_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class ExecutionResult:
    mission_id: str
    status: str
    steps: list[dict[str, Any]]
    context: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
