"""Longest dependency chains over the condensed graph."""

from __future__ import annotations

from collections import defaultdict, deque

from .graph import DirectedGraph


def longest_chains(
    graph: DirectedGraph,
    components: list[list[str]],
    *,
    limit: int = 10,
) -> list[list[str]]:
    component_index: dict[str, int] = {}
    for index, component in enumerate(components):
        for node in component:
            component_index[node] = index

    outgoing: dict[int, set[int]] = defaultdict(set)
    incoming_count: dict[int, int] = {index: 0 for index in range(len(components))}

    for source in graph.nodes:
        source_component = component_index[source]
        for target in graph.outgoing.get(source, set()):
            target_component = component_index[target]
            if source_component == target_component:
                continue
            if target_component not in outgoing[source_component]:
                outgoing[source_component].add(target_component)
                incoming_count[target_component] += 1

    queue = deque(
        sorted(index for index, count in incoming_count.items() if count == 0)
    )
    best: dict[int, list[int]] = {index: [index] for index in incoming_count}

    while queue:
        current = queue.popleft()
        for target in sorted(outgoing.get(current, set())):
            candidate = [*best[current], target]
            if len(candidate) > len(best.get(target, [])):
                best[target] = candidate
            incoming_count[target] -= 1
            if incoming_count[target] == 0:
                queue.append(target)

    ranked = sorted(
        best.values(),
        key=lambda chain: (-len(chain), chain),
    )

    rendered: list[list[str]] = []
    seen: set[tuple[int, ...]] = set()
    for chain in ranked:
        key = tuple(chain)
        if key in seen:
            continue
        seen.add(key)
        rendered.append([" | ".join(components[index]) for index in chain])
        if len(rendered) >= limit:
            break
    return rendered
