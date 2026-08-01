import json

from aletheus.tooling.engine_activation.engine import ActivationManager


def test_activation_manager_activates_registered_engines(tmp_path) -> None:
    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps({"engines": [{"engine_name": "Evidence Engine"}]}))
    report = ActivationManager(registry, tmp_path / "out").activate_all()
    assert report["activated_count"] == 1
    assert report["failed_count"] == 0
