from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class RuntimeLayer(str, Enum):
    CONSTITUTION = "constitution"
    FOUNDATION = "foundation"
    INFRASTRUCTURE = "infrastructure"
    CAPABILITY_DOMAIN = "capability_domain"
    PLATFORM_SERVICE = "platform_service"
    ENGINE = "engine"
    APPLICATION = "application"


class ComponentHealth(str, Enum):
    INITIALIZING = "initializing"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class RuntimeCharacteristic(str, Enum):
    EXPLAINABLE = "explainable"
    ADAPTIVE = "adaptive"
    NIMBLE = "nimble"
    ELASTIC = "elastic"
    OBSERVABLE = "observable"
    GOVERNED = "governed"
    RESILIENT = "resilient"
    EFFICIENT = "efficient"


@dataclass
class RuntimeComponent:
    """
    Canonical component manifest for AletheusOS.

    Every subsystem should eventually expose one of these.
    """

    component_id: str
    name: str
    layer: RuntimeLayer
    purpose: str

    version: str = "0.1"
    health: ComponentHealth = ComponentHealth.UNKNOWN

    dependencies: list[str] = field(default_factory=list)
    provides: list[str] = field(default_factory=list)

    runtime_characteristics: list[RuntimeCharacteristic] = field(
        default_factory=list
    )

    owner: str = "AletheusOS"
    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass
class RuntimeRegistryReport:
    status: str
    component_count: int
    healthy_count: int
    degraded_count: int
    unavailable_count: int
    unknown_count: int
    generated_at: str = field(default_factory=utc_now)
