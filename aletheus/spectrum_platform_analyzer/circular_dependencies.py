"""
Spectrum Platform Analyzer
Circular Dependency Analyzer

Genesis 54.4
"""

from __future__ import annotations

from .dependency import dependency_analyzer


class CircularDependencyAnalyzer:

    VERSION = "1.0.0"

    GENESIS = "54.4"

    def normalize_graph(
        self,
        graph: dict[str, list[str]],
    ) -> dict[str, list[str]]:

        modules = set(graph.keys())

        normalized: dict[str, list[str]] = {}

        for module, imports in graph.items():

            internal_imports = []

            for imported in imports:

                if imported in modules:

                    internal_imports.append(imported)

                else:

                    #
                    # Match package-level imports to known modules.
                    #

                    matches = [
                        candidate
                        for candidate in modules
                        if candidate.startswith(f"{imported}.")
                    ]

                    internal_imports.extend(matches)

            normalized[module] = sorted(set(internal_imports))

        return normalized

    def detect_cycles(
        self,
        graph: dict[str, list[str]],
    ) -> list[list[str]]:

        visited: set[str] = set()

        stack: set[str] = set()

        path: list[str] = []

        cycles: list[list[str]] = []

        def visit(node: str):

            if node in stack:

                index = path.index(node)

                cycle = path[index:] + [node]

                if cycle not in cycles:

                    cycles.append(cycle)

                return

            if node in visited:

                return

            visited.add(node)

            stack.add(node)

            path.append(node)

            for neighbor in graph.get(node, []):

                visit(neighbor)

            stack.remove(node)

            path.pop()

        for node in graph:

            visit(node)

        return cycles

    def analyze(
        self,
        root: str,
    ) -> list[dict]:

        graph = dependency_analyzer.internal_import_graph(root)

        normalized = self.normalize_graph(graph)

        cycles = self.detect_cycles(normalized)

        return [
            {
                "cycle": cycle,
                "length": len(cycle) - 1,
                "severity": (
                    "HIGH"
                    if len(cycle) > 4
                    else "MEDIUM"
                ),
            }
            for cycle in cycles
        ]

    def summary(
        self,
        root: str,
    ) -> dict:

        cycles = self.analyze(root)

        return {
            "circular_dependencies": len(cycles),
            "status": (
                "PASS"
                if len(cycles) == 0
                else "REVIEW"
            ),
        }

    def health(self) -> dict:

        return {
            "name": "Circular Dependency Analyzer",
            "version": self.VERSION,
            "genesis": self.GENESIS,
            "status": "healthy",
        }


circular_dependency_analyzer = CircularDependencyAnalyzer()
