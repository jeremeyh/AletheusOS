import json

from aletheus.tooling.runtime_flow_visualizer.engine import FlowVisualizerEngine


def test_flow_visualizer_marks_contracts(tmp_path) -> None:
    wiring = tmp_path / "wiring.json"
    contracts = tmp_path / "contracts.json"
    wiring.write_text(json.dumps({"routes": [{"source": "A", "target": "B"}]}))
    contracts.write_text(json.dumps({"contracts": [{"channel_id": "bus::A::B"}]}))
    result = FlowVisualizerEngine(wiring, contracts, tmp_path / "out").build()
    assert result["flows"][0]["contract_present"] is True
