import json

from aletheus.tooling.mission_execution_graph.engine import Engine


def test_graph_builds_edges(tmp_path) -> None:
    source = tmp_path / "orchestration.json"
    source.write_text(json.dumps({"units": [{"unit_id": "a"}, {"unit_id": "b"}]}))
    result = Engine(source, tmp_path / "out").build()
    assert len(result["edges"]) == 1
