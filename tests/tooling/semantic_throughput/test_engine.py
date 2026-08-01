import json

from aletheus.tooling.semantic_throughput.engine import Engine


def test_optimizer_batches_routes(tmp_path) -> None:
    wiring = tmp_path / "wiring.json"
    contracts = tmp_path / "contracts.json"
    braces = tmp_path / "braces.json"
    telemetry = tmp_path / "telemetry.json"
    wiring.write_text(json.dumps({"routes": [{} for _ in range(130)]}))
    contracts.write_text(json.dumps({"contract_count": 130}))
    braces.write_text(json.dumps({"brace_count": 2}))
    telemetry.write_text(json.dumps({"record_count": 130}))
    report = Engine(wiring, contracts, braces, telemetry, tmp_path / "out").build()
    assert report["batch_count"] == 3
    assert report["semantic_continuity_preserved"] is True
