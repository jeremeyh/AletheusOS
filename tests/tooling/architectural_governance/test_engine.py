import json

from aletheus.tooling.architectural_governance.engine import GovernanceEngine


def test_governance_warns_on_high_findings(tmp_path) -> None:
    authority = tmp_path / "authority.json"
    boundary = tmp_path / "boundary.json"
    health = tmp_path / "health.json"
    registry = tmp_path / "registry.json"
    authority.write_text(json.dumps({"findings": []}))
    boundary.write_text(json.dumps({"findings": [{"severity": "high", "code": "X"}]}))
    health.write_text(json.dumps({"readiness": "conditional"}))
    registry.write_text(json.dumps({}))
    report = GovernanceEngine(
        authority, boundary, health, registry, tmp_path / "out"
    ).evaluate()
    assert report["decision"] == "warn"
