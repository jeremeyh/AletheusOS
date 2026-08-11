from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Iterable
from .common import RSFValidationError, utc_now_iso

class MetricDirection(str, Enum):
    MAXIMUM = "MAXIMUM"
    MINIMUM = "MINIMUM"
    BOOLEAN_TRUE = "BOOLEAN_TRUE"

@dataclass(frozen=True)
class ReliabilityObservation:
    observation_id: str
    component_id: str
    metric_id: str
    value: float
    unit: str
    threshold: float
    direction: MetricDirection
    observed_at_iso: str
    passed: bool

@dataclass(frozen=True)
class ObservationSummary:
    component_id: str
    total: int
    passed: int
    failed: int
    degraded: bool

class RuntimeReliabilityObservationFabric:
    @staticmethod
    def observe(
        observation_id: str,
        component_id: str,
        metric_id: str,
        value: float,
        *,
        unit: str,
        threshold: float,
        direction: MetricDirection,
    ) -> ReliabilityObservation:
        if not observation_id or not component_id or not metric_id:
            raise RSFValidationError("observation_id, component_id and metric_id are required")
        if direction is MetricDirection.MAXIMUM:
            passed = value <= threshold
        elif direction is MetricDirection.MINIMUM:
            passed = value >= threshold
        else:
            passed = bool(value) is True
        return ReliabilityObservation(
            observation_id, component_id, metric_id, float(value), unit, float(threshold),
            direction, utc_now_iso(), passed
        )

    @staticmethod
    def summarize(component_id: str, observations: Iterable[ReliabilityObservation]) -> ObservationSummary:
        relevant = tuple(o for o in observations if o.component_id == component_id)
        passed = sum(1 for o in relevant if o.passed)
        failed = len(relevant) - passed
        return ObservationSummary(component_id, len(relevant), passed, failed, failed > 0)
