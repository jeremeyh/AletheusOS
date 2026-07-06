from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def now() -> str:
    return datetime.now(UTC).isoformat()


def new_resolution_id() -> str:
    return f"FSB-{uuid4().hex[:12].upper()}"


@dataclass(slots=True)
class FoundationExecutionStage:
    order: int
    stage_id: str
    name: str
    engine_id: str
    required: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "order": self.order,
            "stage_id": self.stage_id,
            "name": self.name,
            "engine_id": self.engine_id,
            "required": self.required,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class FoundationExecutionPlan:
    plan_id: str
    capability_id: str
    name: str
    engine_id: str
    stages: list[FoundationExecutionStage] = field(default_factory=list)
    constitutional_articles: list[str] = field(default_factory=list)
    expected_outputs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "capability_id": self.capability_id,
            "name": self.name,
            "engine_id": self.engine_id,
            "stages": [stage.to_dict() for stage in self.stages],
            "constitutional_articles": self.constitutional_articles,
            "expected_outputs": self.expected_outputs,
        }


@dataclass(slots=True)
class FoundationCapability:
    capability_id: str
    name: str
    engine_id: str
    description: str = ""
    aliases: list[str] = field(default_factory=list)
    constitutional_articles: list[str] = field(default_factory=list)
    execution_plan: FoundationExecutionPlan | None = None
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "name": self.name,
            "engine_id": self.engine_id,
            "description": self.description,
            "aliases": self.aliases,
            "constitutional_articles": self.constitutional_articles,
            "execution_plan": self.execution_plan.to_dict() if self.execution_plan else None,
            "enabled": self.enabled,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class CapabilityResolution:
    resolution_id: str
    requested_capability: str
    resolved: bool
    capability_id: str | None = None
    name: str | None = None
    engine_id: str | None = None
    execution_plan: FoundationExecutionPlan | None = None
    reason: str = ""
    confidence: float = 1.0
    alternatives: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "resolution_id": self.resolution_id,
            "requested_capability": self.requested_capability,
            "resolved": self.resolved,
            "capability_id": self.capability_id,
            "name": self.name,
            "engine_id": self.engine_id,
            "execution_plan": self.execution_plan.to_dict() if self.execution_plan else None,
            "reason": self.reason,
            "confidence": self.confidence,
            "alternatives": self.alternatives,
            "timestamp": self.timestamp,
        }
