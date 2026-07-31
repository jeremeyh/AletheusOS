from __future__ import annotations

from .registry import OverlayRegistry


class OverlayResolver:
    GENESIS = "21.5"
    VERSION = "0.1.0"

    def __init__(self, registry: OverlayRegistry):
        self.registry = registry

    def resolve(self, application: str, value: str):
        app_overlays = self.registry.get_application(application)

        if value in app_overlays:
            return value

        for definition in app_overlays.values():
            if definition.display_name == value:
                return definition.foundation_engine

        return value

    def presentation(self, application: str, foundation_engine: str):
        app_overlays = self.registry.get_application(application)

        definition = app_overlays.get(foundation_engine)

        return (
            definition.to_dict()
            if definition
            else {
                "foundation_engine": foundation_engine,
                "display_name": foundation_engine,
                "visible": True,
            }
        )
