import json

from aletheus.tooling.engine_registry_realization.engine import Engine


def test_engine_registry_realizes_engines(tmp_path) -> None:
    catalog = tmp_path / "catalog.json"
    contracts = tmp_path / "contracts.json"
    bus = tmp_path / "bus.json"
    catalog.write_text(
        json.dumps(
            {
                "entries": [
                    {
                        "name": "Evidence Engine",
                        "category": "core_intelligence",
                        "mesh_connections": ["Knowledge Engine"],
                    }
                ]
            }
        )
    )
    contracts.write_text(json.dumps({"contracts": []}))
    bus.write_text(json.dumps({"channels": []}))
    result = Engine(catalog, contracts, bus, tmp_path / "out").build()
    assert result["engine_count"] == 1
