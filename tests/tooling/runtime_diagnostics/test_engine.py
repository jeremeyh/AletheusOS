import json

from aletheus.tooling.runtime_diagnostics.engine import Engine


def test_diagnostics_detect_not_ready(tmp_path) -> None:
    observability = tmp_path / "observability.json"
    governance = tmp_path / "governance.json"
    observability.write_text(json.dumps({"readiness": "not_ready"}))
    governance.write_text(json.dumps({"decision": "pass"}))
    result = Engine(observability, governance, tmp_path / "out").build()
    assert result["diagnostic_count"] == 1
