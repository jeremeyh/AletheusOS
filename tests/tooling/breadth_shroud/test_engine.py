import json

from aletheus.tooling.breadth_shroud.engine import Engine


def test_breadth_does_not_own_decisions(tmp_path) -> None:
    catalog = tmp_path / "catalog.json"
    graph = tmp_path / "graph.json"
    observability = tmp_path / "observability.json"
    catalog.write_text(json.dumps({"entries": []}))
    graph.write_text(json.dumps({"nodes": []}))
    observability.write_text(json.dumps({"readiness": "ready"}))
    result = Engine(catalog, graph, observability, tmp_path / "out").build()
    assert result["owns_decisions"] is False
