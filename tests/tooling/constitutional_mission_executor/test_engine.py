import json

from aletheus.tooling.constitutional_mission_executor.engine import Engine


def test_executor_is_approval_gated(tmp_path) -> None:
    orchestrator = tmp_path / "orchestrator.json"
    graph = tmp_path / "graph.json"
    bus = tmp_path / "bus.json"
    orchestrator.write_text(json.dumps({"units": [{"unit_id": "u1"}]}))
    graph.write_text(json.dumps({"nodes": [{"node_id": "u1"}]}))
    bus.write_text(json.dumps({"channels": [{"channel_id": "c"}]}))
    result = Engine(orchestrator, graph, bus, tmp_path / "out").build()
    assert result["mode"] == "approval_gated"
    assert result["missions"][0]["execution_enabled"] is False
