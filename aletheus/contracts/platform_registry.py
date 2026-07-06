from __future__ import annotations

from .platform_component import PlatformComponent


class PlatformRegistry:
    """
    Platform Registry™

    Canonical registry for all Platform Components.
    """

    GENESIS = "6.8"
    VERSION = "0.2.0"

    def __init__(self):
        self._components: dict[str, PlatformComponent] = {}

    def register(self, component: PlatformComponent):
        self._components[component.COMPONENT_ID] = component
        return component

    def get(self, component_id: str):
        return self._components.get(component_id)

    def list(self):
        return list(self._components.values())

    def ids(self):
        return sorted(self._components.keys())

    def count(self):
        return len(self._components)

    def metadata(self):
        return [component.metadata() for component in self.list()]

    def health(self):
        return [component.health() for component in self.list()]

    def capabilities(self):
        return {
            component.COMPONENT_ID: component.capabilities()
            for component in self.list()
        }

    def dependencies(self):
        return {
            component.COMPONENT_ID: component.dependencies()
            for component in self.list()
        }

    def statistics(self):
        return {
            "name": "Platform Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "registered_components": self.count(),
            "component_ids": self.ids(),
        }
