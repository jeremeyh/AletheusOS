from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class SurfaceKind(StrEnum):
    ROOM = "ROOM"
    PLATFORM_OVERLAY = "PLATFORM_OVERLAY"
    SYSTEM_SURFACE = "SYSTEM_SURFACE"


class SurfaceState(StrEnum):
    DORMANT = "DORMANT"
    HYDRATING = "HYDRATING"
    READY = "READY"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class HydrationSource:
    capability: str
    required: bool = True
    freshness_seconds: int = 300


@dataclass(frozen=True, slots=True)
class ExperienceAction:
    action_id: str
    label: str
    intent: str
    requires_confirmation: bool = False
    destination: str | None = None


@dataclass(frozen=True, slots=True)
class ExperienceSurface:
    surface_id: str
    display_name: str
    description: str
    kind: SurfaceKind
    hydration_sources: tuple[HydrationSource, ...] = ()
    overlays: tuple[str, ...] = ()
    actions: tuple[ExperienceAction, ...] = ()
    permissions: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ExperienceSession:
    session_id: str
    active_surface_id: str
    state: SurfaceState
    surface_stack: tuple[str, ...] = ()
    overlay_stack: tuple[str, ...] = ()
    context: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CompositionResult:
    session: ExperienceSession
    surface: ExperienceSurface
    resolved_overlays: tuple[str, ...]
    hydration_plan: tuple[HydrationSource, ...]
    warnings: tuple[str, ...] = ()
