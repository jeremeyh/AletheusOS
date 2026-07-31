"""Models for Kinekt™ evolution orchestration."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ExecutionUnit:
    unit_id: str
    title: str
    phase: int
    category: str
    candidate_ids: tuple[str, ...]
    risk: str
    effort: str
    expected_health_gain: float
    preconditions: tuple[str, ...]
    validations: tuple[str, ...]
    rollback_requirements: tuple[str, ...]
    approval_required: bool = True


@dataclass(slots=True)
class ExecutionManifest:
    generated_at: str
    source_roadmap: str
    status: str
    units: list[ExecutionUnit] = field(default_factory=list)
    abstentions: list[str] = field(default_factory=list)
    provenance: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
