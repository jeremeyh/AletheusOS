from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any


@dataclass(frozen=True, slots=True)
class TopologySnapshot:
    version: str
    domains: tuple[str, ...]
    services: tuple[str, ...]
    components: tuple[str, ...]
    providers: tuple[str, ...]
    capabilities: tuple[str, ...]
    dependencies: Mapping[str, tuple[str, ...]]
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "domains": list(self.domains),
            "services": list(self.services),
            "components": list(self.components),
            "providers": list(self.providers),
            "capabilities": list(self.capabilities),
            "dependencies": {
                name: list(values) for name, values in self.dependencies.items()
            },
            "metadata": dict(self.metadata),
        }
