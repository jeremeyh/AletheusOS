import json

from aletheus.tooling.capability_dependency_graph.engine import Engine


def test_capability_graph(tmp_path) -> None:
    authority = tmp_path / "a.json"
    registry = tmp_path / "r.json"
    authority.write_text(
        json.dumps({"capabilities": [{"name": "A"}]}),
        encoding="utf-8",
    )
    registry.write_text(
        json.dumps({"engines": [{"engine_name": "A"}]}),
        encoding="utf-8",
    )
    report = Engine(authority, registry, tmp_path / "out").build()
    assert report["implemented_count"] == 1
