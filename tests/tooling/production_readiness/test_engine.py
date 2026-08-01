import json

from aletheus.tooling.production_readiness.engine import Engine


def test_ready_certification(tmp_path) -> None:
    health = tmp_path / "h.json"
    compatibility = tmp_path / "c.json"
    health.write_text(json.dumps({"healthy": True}), encoding="utf-8")
    compatibility.write_text(
        json.dumps({"incompatible_count": 0}),
        encoding="utf-8",
    )
    report = Engine(health, compatibility, tmp_path / "out").certify()
    assert report["status"] == "READY"
