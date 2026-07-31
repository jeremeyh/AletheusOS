from __future__ import annotations


class ComponentGraph:
    """
    Component Graph™

    Represents dependencies between AletheusOS platform
    components. This graph will eventually drive automatic
    boot ordering, restart planning, dependency inspection,
    and impact analysis.
    """

    GENESIS = "6.7"

    VERSION = "0.1.0"

    def __init__(self):
        self._edges: dict[str, set[str]] = {}

    def add_component(self, component_id: str):

        self._edges.setdefault(component_id, set())

    def connect(self, source: str, target: str):

        self.add_component(source)
        self.add_component(target)

        self._edges[source].add(target)

    def dependencies_of(self, component_id: str):

        return sorted(self._edges.get(component_id, set()))

    def dependents_of(self, component_id: str):

        return sorted(
            source for source, targets in self._edges.items() if component_id in targets
        )

    def nodes(self):

        return sorted(self._edges.keys())

    def statistics(self):

        return {
            "name": "Component Graph",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "components": len(self._edges),
            "dependencies": sum(len(v) for v in self._edges.values()),
        }

    def health(self):

        return {
            "name": "Component Graph",
            "status": "online",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "components": len(self._edges),
        }
