import json

from aletheus.tooling.data_contracts.engine import DataContractEngine


def test_contracts_require_provenance(tmp_path) -> None:
    bus = tmp_path / "bus.json"
    bus.write_text(json.dumps({"channels": [{"channel_id": "x"}]}))
    result = DataContractEngine(bus, tmp_path / "out").build()
    assert "provenance" in result["contracts"][0]["required_fields"]
