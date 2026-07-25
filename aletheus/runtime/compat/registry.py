from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class RuntimeService:

    alias: str
    implementation: Any
    version: str
    capabilities: list[str] = field(default_factory=list)


class CompatibilityRegistry:

    VERSION = "4.1.0"

    def __init__(self):

        self.services: dict[str, RuntimeService] = {}

    def register(
        self,
        alias: str,
        implementation: Any,
        capabilities=None,
    ):

        service = RuntimeService(
            alias=alias,
            implementation=implementation,
            version=getattr(
                implementation,
                "VERSION",
                getattr(
                    implementation,
                    "version",
                    "unknown",
                ),
            ),
            capabilities=capabilities or [],
        )

        self.services[alias] = service

        return asdict(service)

    def resolve(self, alias):

        if alias not in self.services:
            raise KeyError(alias)

        return self.services[alias].implementation

    def list(self):

        return [
            asdict(service)
            for service in self.services.values()
        ]

    def statistics(self):

        return {
            "version": self.VERSION,
            "registered": len(self.services),
            "services": len(self.services),
            "aliases": sorted(self.services.keys()),
            "health": "healthy",
        }


compatibility_registry = CompatibilityRegistry()
