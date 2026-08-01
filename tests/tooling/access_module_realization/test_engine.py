import json

from aletheus.tooling.access_module_realization.engine import Engine


def test_access_modules_require_auth(tmp_path) -> None:
    connectors = tmp_path / "connectors.json"
    contracts = tmp_path / "contracts.json"
    connectors.write_text(
        json.dumps(
            {"connectors": [{"source": "A", "target": "B", "connector_id": "x"}]}
        )
    )
    contracts.write_text(json.dumps({"contracts": [{"channel_id": "bus::A::B"}]}))
    result = Engine(connectors, contracts, tmp_path / "out").build()
    assert result["access_modules"][0]["authorization_required"] is True
