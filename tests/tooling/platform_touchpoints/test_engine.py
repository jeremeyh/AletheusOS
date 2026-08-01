import json

from aletheus.tooling.platform_touchpoints.engine import Engine


def test_touchpoints_build(tmp_path) -> None:
    access = tmp_path / "access.json"
    graph = tmp_path / "graph.json"
    access.write_text(
        json.dumps({"access_modules": [{"connector_id": "x", "access_module_id": "a"}]})
    )
    graph.write_text(json.dumps({"nodes": [{"node_id": "n"}]}))
    result = Engine(access, graph, tmp_path / "out").build()
    assert result["touchpoint_count"] == 1
