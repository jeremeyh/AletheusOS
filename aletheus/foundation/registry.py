from __future__ import annotations

from .models import FoundationEngine


class FoundationEngineRegistry:
    GENESIS = "16.2"
    VERSION = "0.1.0"

    def __init__(self):
        self._engines: dict[str, FoundationEngine] = {}

    def register(self, engine: FoundationEngine):
        self._engines[engine.engine_id] = engine
        return engine

    def get(self, engine_id: str):
        return self._engines.get(engine_id)

    def list(self):
        return [engine.to_dict() for engine in self._engines.values()]

    def count(self):
        return len(self._engines)

    def health(self):
        return {
            "name": "Aletheus Foundation Engine Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "engines": self.count(),
        }

    def statistics(self):
        return {
            "engines": self.count(),
            "engine_ids": sorted(self._engines.keys()),
        }
