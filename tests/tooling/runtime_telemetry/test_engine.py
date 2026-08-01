import json

from aletheus.tooling.runtime_telemetry.engine import Engine


def test_telemetry_builds_records(tmp_path) -> None:
    graph = tmp_path / "graph.json"
    graph.write_text(json.dumps({"nodes": [{"node_id": "a"}]}))
    result = Engine(graph, tmp_path / "out").build()
    assert result["record_count"] == 1
