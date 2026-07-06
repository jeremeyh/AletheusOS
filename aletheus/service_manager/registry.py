from __future__ import annotations

from .models import ServiceRegistration


class ServiceRegistry:
    GENESIS = "8.2"
    VERSION = "0.1.0"

    def __init__(self):
        self._services: dict[str, ServiceRegistration] = {}

    def register(self, service: ServiceRegistration):
        self._services[service.service_id] = service
        return service

    def get(self, service_id: str):
        return self._services.get(service_id)

    def list(self):
        return sorted(
            self._services.values(),
            key=lambda service: service.priority,
        )

    def count(self):
        return len(self._services)

    def statistics(self):
        return {
            "name": "Service Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "services": self.count(),
            "critical": sum(1 for s in self._services.values() if s.critical),
        }
