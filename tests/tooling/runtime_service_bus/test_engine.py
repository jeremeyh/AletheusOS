import json

from aletheus.tooling.runtime_service_bus.engine import ServiceBusEngine


def test_service_bus_builds_channels(tmp_path) -> None:
    wiring = tmp_path / "wiring.json"
    wiring.write_text(json.dumps({"routes": [{"source": "A", "target": "B"}]}))
    result = ServiceBusEngine(wiring, tmp_path / "out").build()
    assert result["channel_count"] == 1
