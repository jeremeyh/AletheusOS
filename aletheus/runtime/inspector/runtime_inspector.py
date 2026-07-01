"""
Runtime Inspector

Version 5.2.0
"""

from __future__ import annotations

import inspect


class RuntimeInspector:

    def __init__(self, runtime):
        self.runtime = runtime

    def handlers(self):

        handlers = []

        for name, member in inspect.getmembers(self.runtime):

            if callable(member) and name.startswith("_cmd_"):
                handlers.append(name)

        return sorted(handlers)

    def services(self):

        if not hasattr(self.runtime, "services"):
            return []

        stats = self.runtime.services.statistics()

        return stats.get("services", [])

    def summary(self):

        return {
            "version": self.runtime.version,
            "status": self.runtime.status,
            "handlers": len(self.handlers()),
            "services": len(self.services()),
        }
