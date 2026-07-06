from __future__ import annotations

from aletheus.contracts import PlatformRegistry, PlatformComponent


class RegistryService:
    GENESIS = "6.7"
    VERSION = "0.1.0"

    def __init__(self):
        self.registry = PlatformRegistry()

    def register(self, component: PlatformComponent):
        return self.registry.register(component)

    def count(self):
        return self.registry.count()

    def health(self):
        return {
            "name": "Registry Service",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "components": self.registry.count(),
        }

    def statistics(self):
        return self.registry.statistics()
