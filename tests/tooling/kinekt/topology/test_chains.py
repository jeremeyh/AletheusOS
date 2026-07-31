from aletheus.tooling.kinekt.topology.chains import longest_chains
from aletheus.tooling.kinekt.topology.graph import DirectedGraph
from aletheus.tooling.kinekt.topology.scc import strongly_connected_components


def test_longest_chain() -> None:
    graph = DirectedGraph()
    graph.add_edge("a", "b")
    graph.add_edge("b", "c")

    components = strongly_connected_components(graph)
    chains = longest_chains(graph, components)

    assert chains[0] == ["a", "b", "c"]
