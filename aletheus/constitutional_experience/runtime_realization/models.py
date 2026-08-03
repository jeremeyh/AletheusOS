from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class RuntimeCapability(StrEnum):
    WEBGPU = "webgpu"
    WASM = "wasm"
    SHARED_ARRAY_BUFFER = "shared_array_buffer"
    MULTI_MONITOR = "multi_monitor"
    REDUCED_MOTION = "reduced_motion"
    FOUNDER_ROOT = "founder_root"


@dataclass(frozen=True, slots=True)
class EvidenceNode:
    node_id: str
    provenance: float
    consensus: float
    utility: float
    veracity: float
    contradiction: float = 0.0
    temporal_delta: float = 0.0


@dataclass(frozen=True, slots=True)
class TelemetryFrame:
    timestamp_ns: int
    fps: float
    frame_time_ms: float
    gpu_queue_depth: int
    wasm_step_ms: float
    mission_health: float
    constitutional_compliance: float
    security_posture: float
    developer_activity: int = 0
    admin_activity: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RuntimeProfile:
    target_fps: int = 120
    physics_hz: int = 120
    respiration_hz: float = 0.15
    max_visible_nodes: int = 4096
    reduced_motion: bool = False
    low_power: bool = False


@dataclass(frozen=True, slots=True)
class RuntimeHealth:
    status: str
    score: float
    bottlenecks: tuple[str, ...]
    recommendations: tuple[str, ...]
