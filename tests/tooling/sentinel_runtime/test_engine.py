import json

from aletheus.tooling.sentinel_runtime.engine import Engine


def test_sentinel_response_is_approval_gated(tmp_path) -> None:
    spartan = tmp_path / "spartan.json"
    observability = tmp_path / "observability.json"
    diagnostics = tmp_path / "diagnostics.json"
    governance = tmp_path / "governance.json"
    spartan.write_text(json.dumps({"integration_mode": "shared_crk_runtime"}))
    observability.write_text(json.dumps({"readiness": "not_ready"}))
    diagnostics.write_text(json.dumps({"diagnostics": []}))
    governance.write_text(json.dumps({"decision": "warn"}))
    result = Engine(
        spartan, observability, diagnostics, governance, tmp_path / "out"
    ).build()
    assert result["autonomous_response_enabled"] is False
