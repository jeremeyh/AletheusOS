from __future__ import annotations

from .registry import foundation_service_registry
from .router import foundation_service_router


class FoundationServiceBus:
    GENESIS = "32.1"
    VERSION = "1.0.0"

    def __init__(self) -> None:
        self.registry = foundation_service_registry
        self.router = foundation_service_router

    def resolve(self, capability: str):
        return self.router.resolve(capability)

    def plan(self, capability: str):
        resolution = self.resolve(capability)
        return resolution.execution_plan

    def capabilities(self) -> list[dict]:
        return [capability.to_dict() for capability in self.registry.list()]

    def health(self) -> dict:
        return {
            "name": "Foundation Service Bus",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
            "registry": self.registry.statistics(),
            "router": self.router.health(),
        }

    def statistics(self) -> dict:
        stats = self.registry.statistics()
        return {
            "name": "Foundation Service Bus",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "capabilities": stats["capabilities"],
            "aliases": stats["aliases"],
        }


foundation_service_bus = FoundationServiceBus()
