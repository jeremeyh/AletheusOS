from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class NavigationMode(StrEnum):
    DIRECT = "DIRECT"
    GRAPH = "GRAPH"
    MISSION = "MISSION"
    CONTEXTUAL = "CONTEXTUAL"


class WorkspacePriority(StrEnum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    AMBIENT = "AMBIENT"
    HIDDEN = "HIDDEN"


@dataclass(frozen=True, slots=True)
class ExperienceNode:
    node_id: str
    display_name: str
    surface_id: str
    node_type: str = "ROOM"
    required_permissions: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ExperienceEdge:
    source: str
    destination: str
    relation: str
    preserve_context: bool = True
    required_overlay: str | None = None


@dataclass(frozen=True, slots=True)
class NavigationContext:
    session_id: str
    current_node: str
    asset_id: str | None = None
    mission_id: str | None = None
    evidence_ids: tuple[str, ...] = ()
    overlays: tuple[str, ...] = ()
    history: tuple[str, ...] = ()
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class MissionContext:
    mission_id: str
    objective: str
    subject: str
    constraints: dict[str, Any] = field(default_factory=dict)
    active: bool = True


@dataclass(frozen=True, slots=True)
class WorkspaceRegion:
    region_id: str
    surface_id: str
    priority: WorkspacePriority
    weight: float = 1.0
    dock: str = "CENTER"


@dataclass(frozen=True, slots=True)
class TimelineEvent:
    event_id: str
    event_type: str
    timestamp: str
    surface_id: str
    subject_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
