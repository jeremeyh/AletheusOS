import json

from aletheus.tooling.kinekt.evolution.loader import load_plan


def test_load_plan(tmp_path) -> None:
    path = tmp_path / "plan.json"
    path.write_text(
        json.dumps(
            {
                "plan_id": "test",
                "summary": "test plan",
                "operations": [
                    {
                        "operation": "write_file",
                        "path": "aletheus/generated.py",
                        "content": "value = 1\n",
                    }
                ],
                "validation": {},
            }
        ),
        encoding="utf-8",
    )

    plan = load_plan(path)

    assert plan.plan_id == "test"
    assert plan.operations[0].operation == "write_file"
