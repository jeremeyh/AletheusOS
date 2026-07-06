from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class CapabilityProviderRecord:
    name: str
    capability: str
    handler: Callable[[dict[str, Any]], Any]
    priority: int = 100
    status: str = "online"
    metadata: dict[str, Any] = field(default_factory=dict)


class CapabilityRegistry:
    """
    AletheusOS Capability Registry™

    Stores and organizes providers for capability-first execution.
    """

    VERSION = "0.1.0"

    def __init__(self):
        self._providers: dict[str, list[CapabilityProviderRecord]] = {}

    def register(
        self,
        name: str,
        capability: str,
        handler: Callable[[dict[str, Any]], Any],
        priority: int = 100,
        metadata: dict[str, Any] | None = None,
    ) -> CapabilityProviderRecord:
        record = CapabilityProviderRecord(
            name=name,
            capability=capability,
            handler=handler,
            priority=priority,
            metadata=metadata or {},
        )

        self._providers.setdefault(capability, []).append(record)
        self._providers[capability].sort(key=lambda item: item.priority)
        return record

    def capabilities(self) -> list[str]:
        return sorted(self._providers.keys())

    def providers_for(self, capability: str) -> list[CapabilityProviderRecord]:
        return list(self._providers.get(capability, []))

    def best_provider(self, capability: str) -> CapabilityProviderRecord | None:
        providers = self.providers_for(capability)
        return providers[0] if providers else None

    def count(self) -> int:
        return sum(len(items) for items in self._providers.values())

    def statistics(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "capabilities": len(self._providers),
            "providers": self.count(),
            "capability_names": self.capabilities(),
        }

    def health(self) -> dict[str, Any]:
        return {
            "name": "Capability Registry",
            "version": self.VERSION,
            "status": "online",
            **self.statistics(),
        }
