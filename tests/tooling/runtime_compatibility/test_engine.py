import json

from aletheus.tooling.runtime_compatibility.engine import Engine


def test_compatibility_matrix(tmp_path) -> None:
    registry = tmp_path / "r.json"
    process = tmp_path / "p.json"
    registry.write_text(
        json.dumps({"engines": [{"engine_name": "A"}]}),
        encoding="utf-8",
    )
    process.write_text(json.dumps({"steps": []}), encoding="utf-8")
    report = Engine(registry, process, tmp_path / "out").build()
    assert report["incompatible_count"] == 0
