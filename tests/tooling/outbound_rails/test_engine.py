import json

from aletheus.tooling.outbound_rails.engine import Engine


def test_outbound_rail_builds(tmp_path) -> None:
    wiring = tmp_path / "wiring.json"
    contracts = tmp_path / "contracts.json"
    wiring.write_text(json.dumps({"routes": [{"source": "A", "target": "B"}]}))
    contracts.write_text(json.dumps({"contracts": [{"channel_id": "bus::A::B"}]}))
    report = Engine(wiring, contracts, tmp_path / "out").build()
    assert report["rail_count"] == 1
