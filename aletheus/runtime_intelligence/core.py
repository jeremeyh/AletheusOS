from __future__ import annotations

from .integration import runtime_intelligence
from .discovery import runtime_engine_discovery


class RuntimeIntelligence:

    GENESIS = "16.5"
    VERSION = "0.1.0"

    def initialize(self):

        return runtime_intelligence.integrate()

    def engines(self):

        return runtime_engine_discovery.discover()

    def health(self):

        return {
            "name": "Runtime Intelligence",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "engines": len(self.engines()),
        }


runtime_intelligence_core = RuntimeIntelligence()
