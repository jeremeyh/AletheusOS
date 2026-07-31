"""
Application Runtime

Version 6.0.0
"""

from __future__ import annotations


class ApplicationRuntime:
    def __init__(self):

        self._applications = {}

    def register(self, name, application):

        self._applications[name] = application

    def unregister(self, name):

        self._applications.pop(name, None)

    def get(self, name):

        return self._applications.get(name)

    def list(self):

        return sorted(self._applications.keys())

    def statistics(self):

        return {
            "registered": len(self._applications),
            "applications": self.list(),
        }
