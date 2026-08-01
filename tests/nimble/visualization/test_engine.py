from aletheus.nimble.visualization.engine import Engine


def test_visualization_catalog() -> None:
    assert {"Gauge", "Graph", "Consensus"} <= {item.name for item in Engine().catalog()}
