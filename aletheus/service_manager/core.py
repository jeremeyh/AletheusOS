from __future__ import annotations

from .models import ServiceRegistration
from .registry import ServiceRegistry
from aletheus.contracts import PlatformComponentContract


class ServiceManager(PlatformComponentContract):
    GENESIS = "13.5"
    VERSION = "0.2.0"

    def __init__(self):
        self.registry = ServiceRegistry()
        self.status_value = "online"

    def boot(self):
        self.status_value = "online"
        return self.health()

    def shutdown(self):
        self.status_value = "offline"
        return self.health()

    def register(
        self,
        service_id: str,
        name: str,
        version: str = "0.1.0",
        priority: int = 100,
        critical: bool = False,
        dependencies: list[str] | None = None,
        metadata: dict | None = None,
    ):
        return self.registry.register(
            ServiceRegistration(
                service_id=service_id,
                name=name,
                version=version,
                priority=priority,
                critical=critical,
                dependencies=dependencies or [],
                metadata=metadata or {},
            )
        )

    def health(self):
        return {
            "name": "Service Manager",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": self.status_value,
            "registry": self.registry.statistics(),
        }

    def statistics(self):
        return {
            "name": "Service Manager",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "services": self.registry.count(),
            "registered": [s.service_id for s in self.registry.list()],
        }


service_manager = ServiceManager()
