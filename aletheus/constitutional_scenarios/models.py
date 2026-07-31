"""Canonical models for the Constitutional Scenario Engine™."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from aletheus.constitutional_cognition import (
    MeshExecutionReport,
)


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def new_scenario_id() -> str:
    return f"SCENARIO-{uuid4().hex[:12].upper()}"


def new_scenario_run_id() -> str:
    return f"SCENARIO-RUN-{uuid4().hex[:12].upper()}"


class AssumptionKind(StrEnum):
    FACT = "fact"
    HYPOTHESIS = "hypothesis"
    CONSTRAINT = "constraint"
    TEMPORAL = "temporal"
    MARKET = "market"
    CONDITION = "condition"


class ScenarioStatus(StrEnum):
    DRAFT = "draft"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    CONTESTED = "contested"
    INSUFFICIENT = "insufficient"
    FAILED = "failed"
    ARCHIVED = "archived"


@dataclass(frozen=True, slots=True)
class ScenarioAssumption:
    """One explicit premise used within a scenario."""

    key: str
    value: Any
    kind: AssumptionKind = AssumptionKind.HYPOTHESIS

    description: str = ""
    confidence: float = 1.0
    source: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("Scenario assumption key may not be blank.")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Scenario assumption confidence must be between 0.0 and 1.0."
            )

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["kind"] = self.kind.value
        return value


@dataclass(frozen=True, slots=True)
class ScenarioDefinition:
    """Immutable definition of one explicit hypothetical branch."""

    scenario_id: str
    canonical_name: str
    assertion_key: str

    assumptions: tuple[ScenarioAssumption, ...]

    description: str = ""
    horizon: str | None = None
    parent_scenario_id: str | None = None

    created_at: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.scenario_id.strip():
            raise ValueError("scenario_id may not be blank.")

        if not self.canonical_name.strip():
            raise ValueError("canonical_name may not be blank.")

        if not self.assertion_key.strip():
            raise ValueError("assertion_key may not be blank.")

        keys = [assumption.key for assumption in self.assumptions]

        if len(keys) != len(set(keys)):
            raise ValueError("Scenario assumptions must have unique keys.")

    def assumption_map(self) -> dict[str, Any]:
        return {assumption.key: assumption.value for assumption in self.assumptions}

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "canonical_name": self.canonical_name,
            "assertion_key": self.assertion_key,
            "description": self.description,
            "horizon": self.horizon,
            "parent_scenario_id": (self.parent_scenario_id),
            "created_at": self.created_at,
            "assumptions": [assumption.to_dict() for assumption in self.assumptions],
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class ScenarioOutcome:
    """Projected outcome produced by a scenario run."""

    scenario_id: str
    run_id: str
    status: ScenarioStatus

    assertion_key: str
    confidence: float

    dominant_stance: str | None
    dissent_count: int
    virtue_score: float

    metrics: dict[str, float]
    report: MeshExecutionReport

    started_at: str
    completed_at: str

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "run_id": self.run_id,
            "status": self.status.value,
            "assertion_key": self.assertion_key,
            "confidence": self.confidence,
            "dominant_stance": self.dominant_stance,
            "dissent_count": self.dissent_count,
            "virtue_score": self.virtue_score,
            "metrics": dict(self.metrics),
            "report": self.report.to_dict(),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class ScenarioMetricDelta:
    metric: str
    baseline_value: float
    scenario_value: float
    absolute_delta: float
    percentage_delta: float | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ScenarioComparison:
    baseline_scenario_id: str
    compared_scenario_id: str

    confidence_delta: float
    virtue_delta: float
    metric_deltas: tuple[ScenarioMetricDelta, ...]

    changed_assumptions: dict[
        str,
        dict[str, Any],
    ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline_scenario_id": (self.baseline_scenario_id),
            "compared_scenario_id": (self.compared_scenario_id),
            "confidence_delta": (self.confidence_delta),
            "virtue_delta": self.virtue_delta,
            "metric_deltas": [delta.to_dict() for delta in self.metric_deltas],
            "changed_assumptions": dict(self.changed_assumptions),
        }
