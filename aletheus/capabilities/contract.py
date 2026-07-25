from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol, runtime_checkable


class CapabilityStatus(str, Enum):
    CREATED = "created"
    REGISTERED = "registered"
    STARTING = "starting"
    READY = "ready"
    ACTIVE = "active"
    DEGRADED = "degraded"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass(slots=True)
class CapabilityMetadata:
    """
    Stable metadata exposed by every AletheusOS capability.

    The platform should reason about capabilities through this metadata,
    not through implementation details.
    """

    capability_id: str
    name: str
    version: str = "1.0.0"
    owner_kernel: str = "runtime"
    provider: str = "unknown"
    description: str = ""
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CapabilityHealthReport:
    """
    Standard health response for platform-hosted capabilities.
    """

    capability_id: str
    status: CapabilityStatus = CapabilityStatus.READY
    score: int = 100
    message: str = "Ready"
    metrics: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CapabilityRequest:
    """
    Standard execution request for a runtime capability.
    """

    capability_id: str
    action: str
    payload: dict[str, Any] = field(default_factory=dict)
    requester: str = "runtime"
    intent_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CapabilityResult:
    """
    Standard execution result returned by a runtime capability.
    """

    capability_id: str
    action: str
    success: bool
    result: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class RuntimeCapability(Protocol):
    """
    Capability Runtime Contract.

    All installable AletheusOS capabilities should satisfy this contract.

    Capabilities do not need to know about runtime/core.py, Executive Kernel,
    managers, or services. The platform hosts capabilities through this
    stable interface.
    """

    def metadata(self) -> CapabilityMetadata:
        ...

    def register(self, runtime: Any) -> None:
        ...

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...

    def health(self) -> CapabilityHealthReport:
        ...

    def execute(
        self,
        request: CapabilityRequest,
    ) -> CapabilityResult:
        ...
