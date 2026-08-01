import json

from aletheus.tooling.validator_composition.engine import Engine


def test_validator_composition_uses_common_interface(tmp_path) -> None:
    consolidation = tmp_path / "consolidation.json"
    consolidation.write_text(json.dumps({"stages": {}}))
    report = Engine(consolidation, tmp_path / "out").build()
    assert report["validator_count"] == 7
    assert report["common_interface"] == "validate(context) -> ValidationResult"
