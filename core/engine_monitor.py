"""
Engine Monitor
"""

from core.engine_registry import engine_registry


class EngineMonitor:
    def report(self):

        rows = {}

        for name, engine in engine_registry.all().items():
            rows[name] = {
                "version": getattr(engine, "version", "unknown"),
                "class": engine.__class__.__name__,
                "module": engine.__class__.__module__,
            }

        return rows


monitor = EngineMonitor()
