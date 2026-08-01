import json

from aletheus.tooling.horizontal_mesh_verifier.engine import Engine


def test_horizontal_mesh_matches_connectors(tmp_path) -> None:
    mesh = tmp_path / "mesh.json"
    connectors = tmp_path / "connectors.json"
    mesh.write_text(json.dumps({"edges": [{}, {}]}))
    connectors.write_text(json.dumps({"connector_count": 2}))
    result = Engine(mesh, connectors, tmp_path / "out").build()
    assert result["horizontal_mesh_connected"] is True
