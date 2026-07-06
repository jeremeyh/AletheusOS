from __future__ import annotations

from aletheus.engine_registry import engine_manager
from aletheus.platform_events import platform_events

from .lifecycle import RuntimeEngineLifecycle


class RuntimeEngineManager:
    GENESIS = "16.4"
    VERSION = "0.1.0"

    def __init__(self):
        self.lifecycle = RuntimeEngineLifecycle()
        self._loaded = False

    def load_foundation_engines(self):
        if self._loaded:
            return self.statistics()

        engine_manager.bootstrap()

        for engine in engine_manager.engines():
            self.lifecycle.register(
                engine_id=engine["engine_id"],
                metadata=engine,
            )

        self._loaded = True

        platform_events.publish(
            "runtime.engines.loaded",
            source="runtime_engine_manager",
            payload={
                "engines": self.lifecycle.count(),
            },
        )

        return self.statistics()

    def start_all(self):
        self.load_foundation_engines()

        results = []

        for state in self.lifecycle.list():
            results.append(
                self.lifecycle.start(
                    state["engine_id"],
                )
            )

        platform_events.publish(
            "runtime.engines.started",
            source="runtime_engine_manager",
            payload={
                "engines": len(results),
            },
        )

        return results

    def stop_all(self):
        results = []

        for state in self.lifecycle.list():
            results.append(
                self.lifecycle.stop(
                    state["engine_id"],
                )
            )

        platform_events.publish(
            "runtime.engines.stopped",
            source="runtime_engine_manager",
            payload={
                "engines": len(results),
            },
        )

        return results

    def health(self):
        online = sum(
            1
            for state in self.lifecycle.list()
            if state["status"] == "online"
        )

        return {
            "name": "Runtime Engine Manager",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "loaded": self._loaded,
            "engines": self.lifecycle.count(),
            "online": online,
        }

    def statistics(self):
        return {
            "name": "Runtime Engine Manager",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "loaded": self._loaded,
            "engines": self.lifecycle.count(),
            "states": self.lifecycle.list(),
        }


runtime_engine_manager = RuntimeEngineManager()
