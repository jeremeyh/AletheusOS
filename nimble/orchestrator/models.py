from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

CapabilityState = Literal[
    "implemented",
    "partial",
    "planned",
    "blocked",
    "missing",
]


@dataclass(frozen=True)
class CapabilityDefinition:
    capability_id: str
    display_name: str
    required_paths: tuple[str, ...]
    dependencies: tuple[str, ...] = ()
    constitutional: bool = False


@dataclass(frozen=True)
class CapabilityStatus:
    capability_id: str
    display_name: str
    state: CapabilityState
    readiness_percent: int
    existing_paths: tuple[str, ...]
    missing_paths: tuple[str, ...]
    dependencies: tuple[str, ...]
    blocked_by: tuple[str, ...]
    constitutional: bool


@dataclass(frozen=True)
class BuildPlanItem:
    order: int
    capability_id: str
    display_name: str
    state: CapabilityState
    action: str
    reason: str
