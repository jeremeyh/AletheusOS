from __future__ import annotations

from aletheus.runtime_engine_manager import runtime_engine_manager


class RuntimeEngineDiscovery:

    def discover(self):

        runtime_engine_manager.load_foundation_engines()

        return runtime_engine_manager.lifecycle.list()


runtime_engine_discovery = RuntimeEngineDiscovery()
