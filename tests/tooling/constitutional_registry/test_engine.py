import json

from aletheus.tooling.constitutional_registry.engine import RegistryEngine


def test_registry_build(tmp_path) -> None:
    authority = tmp_path / "authority.json"
    twin = tmp_path / "twin.json"
    authority.write_text(json.dumps({"capabilities": [{"name": "Kinekt"}]}))
    twin.write_text(json.dumps({"nodes": [{"node_id": "x"}]}))
    result = RegistryEngine(authority, twin, tmp_path / "out").build()
    assert len(result["capabilities"]) == 1
    assert len(result["entities"]) == 1
