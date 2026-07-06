from __future__ import annotations

from .registry import ConstitutionalGraphRegistry


class ConstitutionalGraphTraversal:
    GENESIS = "20.0"
    VERSION = "0.1.0"

    def __init__(self, registry: ConstitutionalGraphRegistry):
        self.registry = registry

    def neighbors(self, node_id: str):
        results = []

        for edge in self.registry.outgoing(node_id):
            target = self.registry.get_node(edge.target_id)
            if target:
                results.append(
                    {
                        "edge": edge.to_dict(),
                        "node": target.to_dict(),
                    }
                )

        return results

    def path_from(self, node_id: str, depth: int = 2):
        visited = set()
        path = []

        def walk(current_id: str, remaining: int):
            if remaining < 0 or current_id in visited:
                return

            visited.add(current_id)

            node = self.registry.get_node(current_id)
            if node:
                path.append(node.to_dict())

            for edge in self.registry.outgoing(current_id):
                path.append(edge.to_dict())
                walk(edge.target_id, remaining - 1)

        walk(node_id, depth)

        return path
