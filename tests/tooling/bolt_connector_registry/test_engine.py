import json

from aletheus.tooling.bolt_connector_registry.engine import Engine


def test_connectors_build(tmp_path) -> None:
    registry = tmp_path / "registry.json"
    wiring = tmp_path / "wiring.json"
    registry.write_text(json.dumps({"engines": [{"engine_name": "A"}]}))
    wiring.write_text(json.dumps({"routes": [{"source": "A", "target": "B"}]}))
    result = Engine(registry, wiring, tmp_path / "out").build()
    assert result["connector_count"] == 1
