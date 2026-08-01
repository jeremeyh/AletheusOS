import json

from aletheus.tooling.runtime_orchestrator.engine import Engine


def test_orchestrator_builds_units(tmp_path) -> None:
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps({"steps": [{"step_id": "step-1"}]}))
    result = Engine(plan, tmp_path / "out").build()
    assert result["unit_count"] == 1
