from __future__ import annotations

from .models import OverlayDefinition


class OverlayRegistry:
    GENESIS = "21.5"
    VERSION = "0.1.0"

    def __init__(self):
        self._overlays: dict[str, dict[str, OverlayDefinition]] = {}

    def register(self, definition: OverlayDefinition):
        app = definition.application

        self._overlays.setdefault(app, {})
        self._overlays[app][definition.foundation_engine] = definition

        return definition

    def get_application(self, application: str):
        return self._overlays.get(application, {})

    def list_application(self, application: str):
        return [
            definition.to_dict()
            for definition in self.get_application(application).values()
        ]

    def all(self):
        results = []

        for application in self._overlays:
            results.extend(self.list_application(application))

        return results

    def count(self):
        return len(self.all())

    def statistics(self):
        return {
            "overlays": self.count(),
            "applications": sorted(self._overlays.keys()),
        }
