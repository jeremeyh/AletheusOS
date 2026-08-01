import json

from aletheus.tooling.spartan_runtime.engine import Engine


def test_spartan_uses_shared_runtime(tmp_path) -> None:
    catalog = tmp_path / "catalog.json"
    bus = tmp_path / "bus.json"
    catalog.write_text(json.dumps({"entries": [{"name": "SPARTAN"}]}))
    bus.write_text(json.dumps({"channels": []}))
    result = Engine(catalog, bus, tmp_path / "out").build()
    assert result["integration_mode"] == "shared_crk_runtime"
