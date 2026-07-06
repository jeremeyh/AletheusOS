from __future__ import annotations

from aletheus.foundation import aletheus_foundation

from .models import IntelligenceEngine
from .registry import EngineRegistry


class IntelligenceEngineManager:

    GENESIS = "16.3"
    VERSION = "0.1.0"

    def __init__(self):

        self.registry = EngineRegistry()

        self._bootstrapped = False

    def bootstrap(self):

        if self._bootstrapped:
            return self.statistics()

        aletheus_foundation.bootstrap_defaults()

        for engine in aletheus_foundation.list_engines():

            self.registry.register(

                IntelligenceEngine(
                    engine_id=engine["engine_id"],
                    name=engine["name"],
                    version="1.0.0",
                    category=engine["category"],
                    foundation_engine=engine["engine_id"],
                    metadata={
                        "aliases": engine["aliases"],
                    },
                )

            )

        self._bootstrapped = True

        return self.statistics()

    def health(self):

        return {
            "name": "Intelligence Engine Manager",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "bootstrapped": self._bootstrapped,
            "registry": self.registry.health(),
        }

    def statistics(self):

        return {
            "name": "Intelligence Engine Manager",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "engines": self.registry.count(),
        }

    def engines(self):

        return self.registry.list()


engine_manager = IntelligenceEngineManager()
