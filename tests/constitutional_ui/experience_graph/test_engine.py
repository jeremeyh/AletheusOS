from aletheus.constitutional_ui.experience_graph.engine import (
    Engine,
    GraphEdge,
    GraphNode,
)


def test_x():
    assert Engine().build(
        (GraphNode("a", "d"), GraphNode("b", "e")), (GraphEdge("b", "a", "supports"),)
    )["valid"]
