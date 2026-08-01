import json

from aletheus.tooling.inbound_rails.engine import Engine


def test_inbound_rail_builds(tmp_path) -> None:
    wiring = tmp_path / "wiring.json"
    access = tmp_path / "access.json"
    wiring.write_text(json.dumps({"routes": [{"source": "A", "target": "B"}]}))
    access.write_text(json.dumps({"access_modules": [{"channel_id": "bus::A::B"}]}))
    report = Engine(wiring, access, tmp_path / "out").build()
    assert report["rail_count"] == 1
