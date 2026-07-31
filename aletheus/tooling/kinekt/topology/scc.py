"""Strongly connected component analysis."""

from __future__ import annotations

from .graph import DirectedGraph


def strongly_connected_components(graph: DirectedGraph) -> list[list[str]]:
    index = 0
    indices: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    components: list[list[str]] = []

    def visit(node: str) -> None:
        nonlocal index
        indices[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for neighbor in sorted(graph.outgoing.get(node, set())):
            if neighbor not in indices:
                visit(neighbor)
                lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
            elif neighbor in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[neighbor])

        if lowlinks[node] == indices[node]:
            component: list[str] = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == node:
                    break
            components.append(sorted(component))

    for node in sorted(graph.nodes):
        if node not in indices:
            visit(node)

    return components


def cycle_groups(graph: DirectedGraph, components: list[list[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    for component in components:
        if (
            len(component) > 1
            or component
            and component[0] in graph.outgoing.get(component[0], set())
        ):
            cycles.append(component)
    return cycles
