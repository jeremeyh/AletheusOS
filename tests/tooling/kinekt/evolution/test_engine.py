import json

from aletheus.tooling.kinekt.evolution.engine import EvolutionEngine


def test_apply_and_rollback(tmp_path) -> None:
    repository = tmp_path / "repo"
    repository.mkdir()
    source = repository / "example.py"
    source.write_text("value = 1\n", encoding="utf-8")

    plan_path = tmp_path / "plan.json"
    plan_path.write_text(
        json.dumps(
            {
                "plan_id": "replace",
                "summary": "replace value",
                "operations": [
                    {
                        "operation": "replace_text",
                        "path": "example.py",
                        "old": "value = 1",
                        "new": "value = 2",
                    }
                ],
                "validation": {},
            }
        ),
        encoding="utf-8",
    )

    engine = EvolutionEngine(repository, tmp_path / "reports")
    result = engine.apply(plan_path, approved=True)

    assert result.status == "applied"
    assert source.read_text(encoding="utf-8") == "value = 2\n"
