import json

from aletheus.tooling.semantic_topology.engine import Engine


def test_semantic_root_classification(tmp_path) -> None:
    paths = tmp_path / "paths.json"
    catalog = tmp_path / "catalog.json"
    paths.write_text(json.dumps({"roots": ["Evidence Engine", "Utility"]}))
    catalog.write_text(json.dumps({"entries": []}))
    report = Engine(paths, catalog, tmp_path / "out").build()
    assert report["root_count"] == 2
    assert "Utility" in report["ambiguous_roots"]
