from __future__ import annotations


class DependencyResolver:
    """
    Genesis 14.3

    AletheusOS Dependency Resolver™

    Consumes a DependencyGraph and produces a deterministic
    dependency-safe boot order.

    Responsibilities
    ----------------
    • Read graph relationships
    • Detect dependency cycles
    • Produce topological boot order
    """

    GENESIS = "14.3"
    VERSION = "0.1.0"

    def resolve(self, graph):
        graph_data = graph.to_dict()

        resolved: list[str] = []
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(component_id: str):
            if component_id in visited:
                return

            if component_id in visiting:
                raise ValueError(
                    f"Dependency cycle detected at {component_id}"
                )

            visiting.add(component_id)

            for dependency_id in graph_data.get(component_id, []):
                visit(dependency_id)

            visiting.remove(component_id)
            visited.add(component_id)
            resolved.append(component_id)

        for component_id in sorted(graph_data.keys()):
            visit(component_id)

        return resolved

    def verify(self, graph):
        try:
            order = self.resolve(graph)

            return {
                "verified": True,
                "order": order,
                "components": len(order),
            }

        except Exception as exc:
            return {
                "verified": False,
                "error": str(exc),
            }

    def health(self):
        return {
            "name": "Dependency Resolver",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
        }

    def statistics(self):
        return self.health()


dependency_resolver = DependencyResolver()
