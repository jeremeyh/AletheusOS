from aletheus.tooling.kinekt.topology.graph import build_graph


def test_graph_building() -> None:
    graph, packages = build_graph(
        [
            {
                "module": "aletheus.alpha",
                "package": "aletheus.alpha",
                "imports": ["aletheus.beta"],
            },
            {
                "module": "aletheus.beta",
                "package": "aletheus.beta",
                "imports": [],
            },
        ]
    )

    assert graph.fan_out("aletheus.alpha") == 1
    assert graph.fan_in("aletheus.beta") == 1
    assert packages["aletheus.alpha"] == "aletheus.alpha"
