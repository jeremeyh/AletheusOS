from __future__ import annotations


class DependencyGraph:
    """
    Genesis 14.2

    AletheusOS Platform Dependency Graph™

    Responsibilities
    ----------------
    • Store component dependencies
    • Validate graph structure
    • Query relationships

    NOTE:
    Boot ordering is NOT performed here.
    That is the responsibility of the
    Dependency Resolver (Genesis 14.3).
    """

    GENESIS = "14.2"
    VERSION = "0.1.0"

    def __init__(self):

        #
        # component_id -> set(dependencies)
        #
        self._graph: dict[str, set[str]] = {}

    # ----------------------------------------------------
    # Registration
    # ----------------------------------------------------

    def add_component(self, component_id: str):

        self._graph.setdefault(component_id, set())

    def add_dependency(
        self,
        component_id: str,
        dependency_id: str,
    ):

        self.add_component(component_id)
        self.add_component(dependency_id)

        self._graph[component_id].add(dependency_id)

    # ----------------------------------------------------
    # Queries
    # ----------------------------------------------------

    def dependencies(self, component_id: str):

        return sorted(
            self._graph.get(component_id, set())
        )

    def dependents(self, component_id: str):

        results = []

        for component, deps in self._graph.items():

            if component_id in deps:
                results.append(component)

        return sorted(results)

    def components(self):

        return sorted(self._graph.keys())

    # ----------------------------------------------------
    # Validation
    # ----------------------------------------------------

    def verify(self):

        #
        # Genesis 14.2
        #
        # Structural validation only.
        # Cycle detection arrives in 14.3.
        #

        return {
            "verified": True,
            "components": len(self._graph),
            "relationships": sum(
                len(v)
                for v in self._graph.values()
            ),
        }

    # ----------------------------------------------------
    # Export
    # ----------------------------------------------------

    def to_dict(self):

        return {
            component: sorted(dependencies)
            for component, dependencies
            in self._graph.items()
        }

    # ----------------------------------------------------
    # Health
    # ----------------------------------------------------

    def health(self):

        return {
            "name": "Platform Dependency Graph",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "components": len(self._graph),
        }

    def statistics(self):

        return {
            "components": len(self._graph),
            "relationships": sum(
                len(v)
                for v in self._graph.values()
            ),
        }


dependency_graph = DependencyGraph()
