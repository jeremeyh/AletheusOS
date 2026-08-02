from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class VeracityPhase(StrEnum):
    NEBULAR = "nebular"
    FLUID = "fluid"
    QUASI_CRYSTALLINE = "quasi_crystalline"
    CRYSTALLINE = "crystalline"


class ExperienceView(StrEnum):
    STANDARD = "standard"
    WORKSPACE_COMPOSER = "workspace_composer"
    ADMIN = "admin"
    DEVELOPER = "developer"
    FOUNDER = "founder"


@dataclass(frozen=True, slots=True)
class EvidenceSignal:
    signal_id: str
    provenance: float
    consensus: float
    value: float
    veracity: float
    contradiction: float = 0.0
    age_seconds: float = 0.0


@dataclass(frozen=True, slots=True)
class ExperienceContext:
    user_id: str
    mission_id: str
    cognitive_load: float = 0.0
    intent_velocity: float = 0.0
    reduced_motion: bool = False
    view: ExperienceView = ExperienceView.STANDARD
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ExperienceProjection:
    phase: VeracityPhase
    informational_mass: float
    density: float
    respiration_hz: float
    tension: float
    motion_scale: float
    provenance_required: bool
    explanations: tuple[str, ...]
