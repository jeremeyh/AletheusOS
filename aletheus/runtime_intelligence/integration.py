from __future__ import annotations

from aletheus.runtime_engine_manager import runtime_engine_manager


class RuntimeIntelligenceIntegration:
    GENESIS = "16.5"
    VERSION = "0.1.0"

    def __init__(self):
        self._integrated = False

    def integrate(self):

        if self._integrated:
            return self.statistics()

        runtime_engine_manager.load_foundation_engines()
        runtime_engine_manager.start_all()

        self._integrated = True

        return self.statistics()

    def statistics(self):

        return {
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "integrated": self._integrated,
            "engines": runtime_engine_manager.lifecycle.count(),
        }


runtime_intelligence = RuntimeIntelligenceIntegration()
