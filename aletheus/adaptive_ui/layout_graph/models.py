from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class DensityLevel(StrEnum):
    AMBIENT_MINIMAL = "AMBIENT_MINIMAL"
    BALANCED = "BALANCED"
    HIGH_DENSITY_FOCUS = "HIGH_DENSITY_FOCUS"
    CRITICAL_CRYSTALLINE = "CRITICAL_CRYSTALLINE"


class TopologicalState(StrEnum):
    NEBULAR_PROBABILITY = "NEBULAR_PROBABILITY"
    FLUID_REACTIVE = "FLUID_REACTIVE"
    QUASI_CRYSTALLINE = "QUASI_CRYSTALLINE"
    CRYSTALLINE_SOLID = "CRYSTALLINE_SOLID"


class CognitiveState(StrEnum):
    CALM = "CALM"
    EXPLORING = "EXPLORING"
    FOCUSED = "FOCUSED"
    OVERLOADED = "OVERLOADED"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True, slots=True)
class TelemetryInput:
    cognitive_load: float
    intent_velocity: float
    system_urgency: float
    focus_depth: float = 0.5
    task_complexity: float = 0.5

    def clamped(self):
        c = lambda v: max(0.0, min(1.0, v))
        return TelemetryInput(
            c(self.cognitive_load),
            c(self.intent_velocity),
            c(self.system_urgency),
            c(self.focus_depth),
            c(self.task_complexity),
        )


@dataclass(frozen=True, slots=True)
class SpatialBounds:
    x: float
    y: float
    z: float
    width: float
    height: float
    depth: float


@dataclass(frozen=True, slots=True)
class PhysicsConfig:
    stiffness: float = 170.0
    damping_ratio: float = 0.9
    mass: float = 1.0
    viscosity: float = 0.5
    magnetic_priority: float = 0.5


@dataclass(frozen=True, slots=True)
class AdaptiveBehavior:
    min_density_visibility: DensityLevel = DensityLevel.AMBIENT_MINIMAL
    on_cognitive_spike: str = "MUTATE_TO_SUMMARY"
    on_high_intent_velocity: str = "CRYSTALLIZE_FACETS"


@dataclass(frozen=True, slots=True)
class LayoutNode:
    node_id: str
    component_type: str
    topological_state: TopologicalState
    bounds: SpatialBounds
    veracity: float = 0.5
    opacity: float = 1.0
    priority: float = 0.5
    behavior: AdaptiveBehavior = field(default_factory=AdaptiveBehavior)
    children: tuple[LayoutNode, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class LayoutScene:
    session_id: str
    density: DensityLevel
    cognitive_state: CognitiveState
    root: LayoutNode
    physics: PhysicsConfig = field(default_factory=PhysicsConfig)
    metadata: dict[str, Any] = field(default_factory=dict)
