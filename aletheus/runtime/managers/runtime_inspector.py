"""
Aletheus Runtime Inspector

Version 5.1.0
"""

from __future__ import annotations

import inspect


class RuntimeInspector:

    def __init__(self, runtime):
        self.runtime = runtime

    def command_handlers(self):

        handlers = []

        for name, member in inspect.getmembers(self.runtime):

            if callable(member) and name.startswith("_cmd_"):

                handlers.append(name)

        return sorted(handlers)

    def registration_summary(self):

        return {
            "handler_count": len(self.command_handlers()),
            "handlers": self.command_handlers(),
        }
