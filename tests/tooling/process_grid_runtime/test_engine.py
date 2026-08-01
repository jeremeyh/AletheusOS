import json

from aletheus.tooling.process_grid_runtime.engine import Engine


def test_process_grid_has_single_final_verdict_stage(tmp_path) -> None:
    validators = tmp_path / "validators.json"
    validators.write_text(json.dumps({"validators": []}))
    report = Engine(validators, tmp_path / "out").build()
    assert report["single_final_verdict_stage"] == "Platform Certification"
    assert report["step_count"] == 17
