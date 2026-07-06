from __future__ import annotations


class ServiceRegistry:
    VERSION = "4.4.0"

    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service

    def get(self, name):
        return self._services.get(name)

    def has(self, name):
        return name in self._services

    def unregister(self, name):
        self._services.pop(name, None)

    def list(self):
        return sorted(self._services.keys())

    def statistics(self):
        return {
            "registered": len(self._services),
            "services": self.list(),
        }
