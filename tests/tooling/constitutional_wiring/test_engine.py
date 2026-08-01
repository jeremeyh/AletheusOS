import json

from aletheus.tooling.constitutional_wiring.engine import WiringEngine


def test_wiring_builds_declared_routes(tmp_path) -> None:
    graph = tmp_path / "graph.json"
    catalog = tmp_path / "catalog.json"
    graph.write_text(json.dumps({"edges": [{"source": "A", "target": "B"}]}))
    catalog.write_text(json.dumps({"entries": [{"name": "A"}, {"name": "B"}]}))
    result = WiringEngine(graph, catalog, tmp_path / "out").build()
    assert result["route_count"] == 1
