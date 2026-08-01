import json

from aletheus.tooling.intelligence_mesh_runtime.engine import Engine


def test_intelligence_mesh_builds_sequence(tmp_path) -> None:
    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps({"engines": []}))
    result = Engine(registry, tmp_path / "out").build()
    assert len(result["routes"]) == 6
