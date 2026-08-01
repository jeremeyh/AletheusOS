import json

from aletheus.tooling.root_domain_resolution.engine import Engine


def test_all_roots_are_resolved(tmp_path) -> None:
    roots = tmp_path / "roots.json"
    catalog = tmp_path / "catalog.json"
    roots.write_text(json.dumps({"roots": [{"node": "Utility"}]}))
    catalog.write_text(json.dumps({"entries": []}))
    report = Engine(roots, catalog, tmp_path / "out").build()
    assert report["resolved_count"] == 1
    assert report["unresolved_roots"] == []
