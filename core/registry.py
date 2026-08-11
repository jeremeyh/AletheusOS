"""
CardHawk OS™
Global Registry
"""


class Registry:
    def __init__(self):
        self.services = {}
        self.engines = {}
        self.providers = {}

    def register_service(self, name, service):
        self.services[name] = service

    def register_engine(self, name, engine):
        self.engines[name] = engine

    def register_provider(self, name, provider):
        self.providers[name] = provider

    def get_service(self, name):
        return self.services.get(name)

    def get_engine(self, name):
        return self.engines.get(name)

    def get_provider(self, name):
        return self.providers.get(name)


registry = Registry()
