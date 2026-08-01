from aletheus.tooling.deployment_policy.engine import Engine


def test_production_policy(tmp_path) -> None:
    report = Engine(tmp_path).evaluate("production", "READY")
    assert report["allowed"] is True
