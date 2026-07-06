from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List


class CapabilityClassification(str, Enum):
    CORE = "core"
    EXECUTIVE = "executive"
    PLATFORM = "platform"
    RUNTIME = "runtime"
    MEMORY = "memory"
    REASONING = "reasoning"
    SECURITY = "security"
    APPLICATION = "application"
    EXPERIMENTAL = "experimental"


class CapabilityTrustLevel(str, Enum):
    CONSTITUTIONAL = "constitutional"
    CERTIFIED = "certified"
    STANDARD = "standard"
    EXPERIMENTAL = "experimental"
    DEPRECATED = "deprecated"


class CapabilityHealth(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    OFFLINE = "offline"
    UNKNOWN = "unknown"


@dataclass(slots=True)
class CapabilityDescriptor:
    capability_id: str
    name: str
    owner_kernel: str
    provider: str
    classification: CapabilityClassification = CapabilityClassification.PLATFORM
    trust_level: CapabilityTrustLevel = CapabilityTrustLevel.STANDARD
    health: CapabilityHealth = CapabilityHealth.UNKNOWN
    version: str = "1.0"
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)


class ExecutiveCapabilityRegistry:
    """
    Registry of executive-visible capability contracts.

    Describes what the platform can do, not how the capability is implemented.
    """

    def __init__(self) -> None:
        self._capabilities: Dict[str, CapabilityDescriptor] = {}

    def register(self, capability: CapabilityDescriptor) -> None:
        self._capabilities[capability.capability_id] = capability

    def unregister(self, capability_id: str) -> None:
        self._capabilities.pop(capability_id, None)

    def get(self, capability_id: str) -> CapabilityDescriptor | None:
        return self._capabilities.get(capability_id)

    def exists(self, capability_id: str) -> bool:
        return capability_id in self._capabilities

    def all(self) -> Iterable[CapabilityDescriptor]:
        return self._capabilities.values()

    def by_kernel(self, kernel_id: str) -> List[CapabilityDescriptor]:
        return [
            capability
            for capability in self._capabilities.values()
            if capability.owner_kernel == kernel_id
        ]

    def count(self) -> int:
        return len(self._capabilities)

    def summary(self) -> dict:
        return {
            "registered_capabilities": self.count(),
            "capabilities": [
                {
                    "id": capability.capability_id,
                    "name": capability.name,
                    "owner_kernel": capability.owner_kernel,
                    "provider": capability.provider,
                    "classification": capability.classification.value,
                    "trust_level": capability.trust_level.value,
                    "health": capability.health.value,
                    "version": capability.version,
                }
                for capability in self._capabilities.values()
            ],
        }
