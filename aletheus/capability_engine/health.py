from __future__ import annotations

from .core import capability_engine


class CapabilityHealth:

    GENESIS = "21.6"
    VERSION = "1.0.0"

    def report(self):

        engine = capability_engine.health()

        return {
            "subsystem": "Capability Engine",
            "status": "healthy",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "components": engine,
        }


capability_health = CapabilityHealth()
