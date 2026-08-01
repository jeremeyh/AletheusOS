import json

from aletheus.tooling.process_composer.engine import Engine


def test_composer_does_not_create_parallel_gate_layer(tmp_path) -> None:
    grid = tmp_path / "grid.json"
    registry = tmp_path / "registry.json"
    authority = tmp_path / "authority.json"
    grid.write_text(json.dumps({"steps": [{"stage": "Telemetry"}]}))
    registry.write_text(json.dumps({"engines": [{"engine_name": "A"}]}))
    authority.write_text(json.dumps({"capabilities": [{"name": "A"}]}))
    report = Engine(grid, registry, authority, tmp_path / "out").build()
    assert report["parallel_gate_layer_created"] is False
    assert report["step_count"] == 1
