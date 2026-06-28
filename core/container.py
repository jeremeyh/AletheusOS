"""
CardHawk OS™
Dependency Injection Container
"""

from core.registry import registry

class Container:

    def __init__(self):
        self._services = {}
        self._engines = {}
        self._providers = {}

    # ---------------- Services ----------------

    def register_service(self, name, service):
        self._services[name] = service
        registry.register_service(name, service)

    def service(self, name):
        return self._services.get(name)

    # ---------------- Engines -----------------

    def register_engine(self, name, engine):
        self._engines[name] = engine
        registry.register_engine(name, engine)

    def engine(self, name):
        return self._engines.get(name)

    # ---------------- Providers ----------------

    def register_provider(self, name, provider):
        self._providers[name] = provider
        registry.register_provider(name, provider)

    def provider(self, name):
        return self._providers.get(name)

    # ---------------- Snapshot ----------------

    def snapshot(self):

        return {
            "services": list(self._services.keys()),
            "engines": list(self._engines.keys()),
            "providers": list(self._providers.keys())
        }

container = Container()
