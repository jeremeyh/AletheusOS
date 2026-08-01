import json

from aletheus.tooling.autonomous_optimization.engine import Engine


def test_optimization_is_advisory_only(tmp_path) -> None:
    diagnostics = tmp_path / "diagnostics.json"
    optimization = tmp_path / "optimization.json"
    diagnostics.write_text(json.dumps({"diagnostic_count": 1}))
    optimization.write_text(json.dumps({"candidates": [{"candidate_id": "one"}]}))
    result = Engine(diagnostics, optimization, tmp_path / "out").build()
    assert result["mode"] == "advisory_only"
    assert result["proposals"][0]["approval_required"] is True
