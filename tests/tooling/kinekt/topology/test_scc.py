from aletheus.tooling.kinekt.topology.graph import DirectedGraph
from aletheus.tooling.kinekt.topology.scc import (
    cycle_groups,
    strongly_connected_components,
)


def test_cycle_detection() -> None:
    graph = DirectedGraph()
    graph.add_edge("a", "b")
    graph.add_edge("b", "a")
    graph.add_node("c")

    components = strongly_connected_components(graph)
    cycles = cycle_groups(graph, components)

    assert ["a", "b"] in cycles
    assert ["c"] not in cycles
