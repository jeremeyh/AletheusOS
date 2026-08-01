import json

from aletheus.tooling.runtime_observability.engine import Engine


def test_observability_combines_inputs(tmp_path) -> None:
    telemetry = tmp_path / "telemetry.json"
    observatory = tmp_path / "observatory.json"
    telemetry.write_text(json.dumps({"record_count": 2}))
    observatory.write_text(json.dumps({"health_score": 50, "readiness": "warn"}))
    result = Engine(telemetry, observatory, tmp_path / "out").build()
    assert result["telemetry_records"] == 2
