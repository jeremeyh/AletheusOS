import json

from aletheus.tooling.realization_gate.engine import RealizationGateEngine


def test_gate_warns_for_disconnected_mesh(tmp_path) -> None:
    ledger = tmp_path / "ledger.json"
    catalog = tmp_path / "catalog.json"
    mesh = tmp_path / "mesh.json"
    governance = tmp_path / "governance.json"

    ledger.write_text(json.dumps({"entries": [{"realized": True}]}))
    catalog.write_text(json.dumps({"entries": [{}, {}]}))
    mesh.write_text(json.dumps({"disconnected": ["One"], "missing_targets": []}))
    governance.write_text(json.dumps({"decision": "warn"}))

    report = RealizationGateEngine(
        ledger, catalog, mesh, governance, tmp_path / "out"
    ).evaluate()
    assert report["decision"] == "warn"
