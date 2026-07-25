"""
CardHawk OS™
Engine Registry
"""

from core.container import container


class EngineRegistry:

    def __init__(self):
        self._engines = {}

    def register(self, name, engine):

        self._engines[name] = engine

        container.register_engine(name, engine)

    def get(self, name):

        return self._engines.get(name)

    def all(self):

        return self._engines

engine_registry = EngineRegistry()
