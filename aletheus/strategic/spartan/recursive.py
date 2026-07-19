"""Recursive intelligence cycle for SPARTAN™."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Mapping
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RecursiveStage(str, Enum):
    OBSERVE = "observe"
    UNDERSTAND = "understand"
    MODEL = "model"
    SIMULATE = "simulate"
    FORECAST = "forecast"
    RECOMMEND = "recommend"
    VALIDATE = "validate"
    LEARN = "learn"
    IMPROVE = "improve"


@dataclass(frozen=True, slots=True)
class RecursiveCycleRecord:
    subject: str
    completed_stages: tuple[RecursiveStage, ...]
    observations: Mapping[str, str] = field(default_factory=dict)
    cycle_id: UUID = field(default_factory=uuid4)
    completed_at: datetime = field(default_factory=utc_now)


class RecursiveIntelligenceCycle:
    """Tracks the canonical SPARTAN recursive cycle.

    Drop 012A records stage progression. Later drops can attach stage handlers,
    simulation providers, model validators, and outcome-learning adapters.
    """

    _ORDER = tuple(RecursiveStage)

    def execute(self, subject: str) -> RecursiveCycleRecord:
        if not subject.strip():
            raise ValueError("Recursive cycle subject must not be empty")

        return RecursiveCycleRecord(
            subject=subject,
            completed_stages=self._ORDER,
            observations={
                stage.value: f"{stage.value.title()} stage completed."
                for stage in self._ORDER
            },
        )
