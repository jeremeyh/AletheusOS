import json

from aletheus.tooling.mesh_synthesis.engine import MeshSynthesisEngine


def test_mesh_detects_disconnected_entry(tmp_path) -> None:
    catalog = tmp_path / "catalog.json"
    catalog.write_text(
        json.dumps(
            {
                "entries": [
                    {"name": "One", "mesh_connections": ["Two"]},
                    {"name": "Two", "mesh_connections": []},
                    {"name": "Three", "mesh_connections": []},
                ]
            }
        )
    )
    result = MeshSynthesisEngine(catalog, tmp_path / "out").build()
    assert result["disconnected"] == ["Three"]
