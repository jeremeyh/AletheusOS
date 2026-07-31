from __future__ import annotations

from enum import StrEnum


class LifecycleState(StrEnum):
    """Canonical lifecycle states for runtime-managed components."""

    CREATED = "created"
    INITIALIZING = "initializing"
    READY = "ready"
    STARTING = "starting"
    RUNNING = "running"
    DEGRADED = "degraded"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"
