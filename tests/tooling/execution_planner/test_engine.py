import json

from aletheus.tooling.execution_planner.engine import Engine


def test_planner_builds_steps(tmp_path) -> None:
    flows = tmp_path / "flows.json"
    flows.write_text(json.dumps({"flows": [{"source": "A", "target": "B"}]}))
    result = Engine(flows, tmp_path / "out").build()
    assert result["step_count"] == 1
