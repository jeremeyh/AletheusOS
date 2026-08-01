from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Mission:
    mission_id: str
    title: str
    status: str
    approval_required: bool
    execution_units: tuple[str, ...]
    preconditions: tuple[str, ...]


@dataclass(slots=True)
class MissionControlReport:
    generated_at: str
    readiness: str
    missions: list[Mission] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
